#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

import duckdb


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_DIR = WORKSPACE_ROOT / 'data' / 'warehouse'
DUCKDB_PATH = WAREHOUSE_DIR / 'biyapay.duckdb'
EXPORT_DIR = WAREHOUSE_DIR / 'extracts'
RAW_XLSX = Path(
    '/Volumes/SSD/Backups/来自：INTEL admin 电脑备份/seoaudition/data/raw/cross/'
    'cross_ga4_3host_hostname_landing_channel_2025-11-20_2026-05-19.xlsx'
)
OUTPUT_CSV = EXPORT_DIR / 'cross_ga4_3host_hostname_landing_channel_2025-11-20_2026-05-19.csv'

MAIN_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PACKAGE_REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'

HEADER_MAP = {
    '主机名': 'hostname',
    '着陆页 + 查询字符串': 'landing_page_query',
    '带来会话的默认渠道组': 'default_channel_group',
    '活跃用户': 'active_users',
    '会话数': 'sessions',
    '关键事件数': 'key_events',
    '事件数': 'event_count',
}


def load_shared_strings(zf: ZipFile) -> list[str]:
    if 'xl/sharedStrings.xml' not in zf.namelist():
        return []
    sst = ET.fromstring(zf.read('xl/sharedStrings.xml'))
    shared = []
    for si in sst.findall(f'{{{MAIN_NS}}}si'):
        shared.append(''.join(node.text or '' for node in si.iter(f'{{{MAIN_NS}}}t')))
    return shared


def workbook_rows(xlsx_path: Path) -> list[list[str]]:
    with ZipFile(xlsx_path) as zf:
        workbook = ET.fromstring(zf.read('xl/workbook.xml'))
        sheet = workbook.find(f'{{{MAIN_NS}}}sheets')[0]
        rel_id = sheet.attrib[f'{{{REL_NS}}}id']
        rels = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
        rel_map = {
            rel.attrib['Id']: rel.attrib['Target']
            for rel in rels.findall(f'{{{PACKAGE_REL_NS}}}Relationship')
        }
        target = rel_map[rel_id]
        if not target.startswith('xl/'):
            target = 'xl/' + target

        shared = load_shared_strings(zf)
        sheet_xml = ET.fromstring(zf.read(target))
        rows_node = sheet_xml.find(f'{{{MAIN_NS}}}sheetData')

        rows = []
        for row in rows_node:
            values = []
            for cell in row:
                cell_type = cell.attrib.get('t')
                value = cell.find(f'{{{MAIN_NS}}}v')
                raw = value.text if value is not None else ''
                if cell_type == 's' and raw:
                    raw = shared[int(raw)]
                values.append(raw)
            rows.append(values)
        return rows


def extract_records(rows: list[list[str]]) -> list[dict[str, str]]:
    header_index = None
    for index, row in enumerate(rows):
        if row[:3] == ['主机名', '着陆页 + 查询字符串', '带来会话的默认渠道组']:
            header_index = index
            break
    if header_index is None:
        raise RuntimeError('Header row not found in landing-channel workbook')

    headers = [HEADER_MAP.get(value, value) for value in rows[header_index]]
    records = []
    for row in rows[header_index + 1 :]:
        if not row or not any(row):
            continue
        first = row[0]
        if first == '总计' or first.startswith('#'):
            continue
        if len(row) != len(headers):
            continue
        record = dict(zip(headers, row))
        if record.get('hostname') in ('', '总计'):
            continue
        records.append(record)
    return records


def write_csv(records: list[dict[str, str]], output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        'hostname',
        'landing_page_query',
        'default_channel_group',
        'active_users',
        'sessions',
        'key_events',
        'event_count',
    ]
    with output_csv.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def import_to_duckdb(output_csv: Path) -> tuple[int, list[tuple[str, str, float, float]]]:
    conn = duckdb.connect(str(DUCKDB_PATH))
    conn.execute('drop table if exists raw_cross_ga4_3host_landing_channel_xlsx')
    conn.execute(
        '''
        create table raw_cross_ga4_3host_landing_channel_xlsx as
        select * from read_csv_auto(?, header=true, all_varchar=true)
        ''',
        [str(output_csv)],
    )
    conn.execute(
        '''
        create or replace view v_cross_ga4_3host_landing_channel as
        select
            hostname,
            landing_page_query,
            default_channel_group,
            cast(nullif(active_users, '') as double) as active_users,
            cast(nullif(sessions, '') as double) as sessions,
            cast(nullif(key_events, '') as double) as key_events,
            cast(nullif(event_count, '') as double) as event_count
        from raw_cross_ga4_3host_landing_channel_xlsx
        '''
    )
    row_count = conn.execute('select count(*) from raw_cross_ga4_3host_landing_channel_xlsx').fetchone()[0]
    preview = conn.execute(
        '''
        select hostname, default_channel_group, round(sum(sessions), 2) as sessions, round(sum(active_users), 2) as active_users
        from v_cross_ga4_3host_landing_channel
        group by 1, 2
        order by sessions desc
        limit 8
        '''
    ).fetchall()
    conn.close()
    return row_count, preview


def main() -> None:
    rows = workbook_rows(RAW_XLSX)
    records = extract_records(rows)
    write_csv(records, OUTPUT_CSV)
    row_count, preview = import_to_duckdb(OUTPUT_CSV)

    print(f'output_csv={OUTPUT_CSV}')
    print(f'imported_rows={row_count}')
    for row in preview:
        print(row)


if __name__ == '__main__':
    main()