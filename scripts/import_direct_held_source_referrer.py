#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import duckdb


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_DIR = WORKSPACE_ROOT / 'data' / 'warehouse'
DUCKDB_PATH = WAREHOUSE_DIR / 'biyapay.duckdb'
NORMALIZED_CSV = WAREHOUSE_DIR / 'extracts' / 'direct_held_source_referrer_normalized.csv'
DEFAULT_SUMMARY = WORKSPACE_ROOT / 'docs' / 'phase3_direct_held_source_referrer_classification_summary.csv'

REQUIRED_COLUMNS = [
    'date',
    'hostname',
    'landing_page_query',
    'default_channel_group',
    'source',
    'medium',
    'full_referrer',
    'sessions',
]

OPTIONAL_COLUMNS = [
    'campaign',
    'source_platform',
    'page_referrer',
    'device_category',
    'country',
]

COLUMN_ALIASES = {
    'date': 'date',
    '日期': 'date',
    'hostname': 'hostname',
    'host name': 'hostname',
    '主机名': 'hostname',
    'landing page + query string': 'landing_page_query',
    'landing_page_query': 'landing_page_query',
    'landing page': 'landing_page_query',
    '着陆页 + 查询字符串': 'landing_page_query',
    'session default channel group': 'default_channel_group',
    'default_channel_group': 'default_channel_group',
    '带来会话的默认渠道组': 'default_channel_group',
    'session source': 'source',
    'source': 'source',
    '会话来源': 'source',
    'session medium': 'medium',
    'medium': 'medium',
    '会话媒介': 'medium',
    'full referrer': 'full_referrer',
    'full_referrer': 'full_referrer',
    '完整引荐来源网址': 'full_referrer',
    'sessions': 'sessions',
    '会话数': 'sessions',
    'campaign': 'campaign',
    'session campaign': 'campaign',
    '广告系列': 'campaign',
    'source platform': 'source_platform',
    'source_platform': 'source_platform',
    'page referrer': 'page_referrer',
    'page_referrer': 'page_referrer',
    'device category': 'device_category',
    'device_category': 'device_category',
    '设备类别': 'device_category',
    'country': 'country',
    '国家/地区': 'country',
}


def normalize_header(value: str) -> str:
    return re.sub(r'\s+', ' ', value.strip().lower())


def canonical_column(value: str) -> str | None:
    return COLUMN_ALIASES.get(normalize_header(value))


def has_utm_param(value: str) -> bool:
    return bool(re.search(r'(^|[?&])utm_[^=&]*=', value.lower()))


def path_group_expr(column_name: str = 'landing_page_query') -> str:
    return f'''
        case
            when {column_name} like '/swift%' or {column_name} like '/en/swift%' or {column_name} like '/zh/swift%' then 'swift'
            when {column_name} like '/blogdetail%' or {column_name} like '/en/blogdetail%' or {column_name} like '/zh/blogdetail%' then 'blogdetail'
            when {column_name} like '/stock%' or {column_name} like '/en/stock%' or {column_name} like '/zh/stock%' then 'stock'
            when {column_name} like '/sendmoney%' or {column_name} like '/en/sendmoney%' or {column_name} like '/zh/sendmoney%' then 'sendmoney'
            when {column_name} like '/compare%' or {column_name} like '/en/compare%' or {column_name} like '/zh/compare%' then 'compare'
            else 'out_of_scope'
        end
    '''


def path_group_for(value: str) -> str:
    for prefix, group in [
        ('/swift', 'swift'),
        ('/blogdetail', 'blogdetail'),
        ('/stock', 'stock'),
        ('/sendmoney', 'sendmoney'),
        ('/compare', 'compare'),
    ]:
        if (
            value.startswith(prefix)
            or value.startswith('/en' + prefix)
            or value.startswith('/zh' + prefix)
        ):
            return group
    return 'out_of_scope'


def validate_scope(rows: list[dict[str, str]]) -> None:
    bad_hosts = sum(1 for row in rows if row.get('hostname') != 'www.biyapay.com')
    bad_channels = sum(
        1
        for row in rows
        if normalize_header(row.get('default_channel_group', '')) != 'direct'
    )
    out_of_scope = sum(
        1
        for row in rows
        if path_group_for(row.get('landing_page_query', '')) == 'out_of_scope'
    )
    errors = []
    if bad_hosts:
        errors.append(f'hostname out of scope rows: {bad_hosts}')
    if bad_channels:
        errors.append(f'default_channel_group out of scope rows: {bad_channels}')
    if out_of_scope:
        errors.append(f'landing_page_query out of scope rows: {out_of_scope}')
    if errors:
        raise ValueError('; '.join(errors))


def read_and_normalize(input_csv: Path) -> list[dict[str, str]]:
    with input_csv.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise RuntimeError(f'No header row found: {input_csv}')
        header_map = {}
        for raw_name in reader.fieldnames:
            canonical = canonical_column(raw_name)
            if canonical:
                header_map[raw_name] = canonical

        found = set(header_map.values())
        missing = [column for column in REQUIRED_COLUMNS if column not in found]
        if missing:
            raise RuntimeError(
                'Missing required columns: ' + ', '.join(missing) + '\n'
                'Required canonical columns: ' + ', '.join(REQUIRED_COLUMNS) + '\n'
                'Input columns: ' + ', '.join(reader.fieldnames)
            )

        output_columns = REQUIRED_COLUMNS + OPTIONAL_COLUMNS
        rows = []
        for input_row in reader:
            output_row = {column: '' for column in output_columns}
            for raw_name, canonical in header_map.items():
                if canonical in output_row:
                    output_row[canonical] = (input_row.get(raw_name) or '').strip()
            rows.append(output_row)
        return rows


def write_normalized(rows: list[dict[str, str]], output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = REQUIRED_COLUMNS + OPTIONAL_COLUMNS
    with output_csv.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def import_to_duckdb(db_path: Path, normalized_csv: Path, summary_csv: Path) -> tuple[int, list[tuple]]:
    conn = duckdb.connect(str(db_path))
    conn.execute('drop table if exists raw_direct_held_source_referrer_import')
    conn.execute(
        '''
        create table raw_direct_held_source_referrer_import as
        select * from read_csv_auto(?, header=true, all_varchar=true)
        ''',
        [str(normalized_csv)],
    )
    conn.execute(
        f'''
        create or replace view v_direct_held_source_referrer_classified as
        with typed as (
            select
                date,
                hostname,
                landing_page_query,
                {path_group_expr()} as path_group,
                default_channel_group,
                lower(coalesce(source, '')) as source_lc,
                lower(coalesce(medium, '')) as medium_lc,
                lower(coalesce(full_referrer, '')) as full_referrer_lc,
                lower(coalesce(page_referrer, '')) as page_referrer_lc,
                lower(coalesce(campaign, '')) as campaign_lc,
                lower(coalesce(source_platform, '')) as source_platform_lc,
                source,
                medium,
                full_referrer,
                campaign,
                source_platform,
                page_referrer,
                device_category,
                country,
                cast(nullif(replace(sessions, ',', ''), '') as double) as sessions
            from raw_direct_held_source_referrer_import
        )
        select
            *,
            case
                when path_group = 'out_of_scope' then 'out_of_scope'
                when campaign_lc not in ('', '(not set)', 'not set', '(none)', 'none')
                  or regexp_matches(lower(landing_page_query), '(^|[?&])utm_[^=&]*=')
                    then 'move_to_campaign_or_promo'
                when regexp_matches(source_platform_lc || ' ' || source_lc || ' ' || medium_lc || ' ' || full_referrer_lc || ' ' || page_referrer_lc,
                    '(app|webview|android|ios|inapp|deep.?link|firebase|mobile)')
                    then 'move_to_app_or_webview_return'
                when medium_lc not in ('', '(not set)', 'not set', '(none)', 'none', 'direct')
                  or source_lc not in ('', '(not set)', 'not set', '(direct)', 'direct', '(none)', 'none')
                  or (
                      full_referrer_lc not in ('', '(not set)', 'not set')
                      and full_referrer_lc not like '%biyapay.com%'
                  )
                    then 'move_to_search_or_referral'
                when source_lc in ('', '(not set)', 'not set', '(direct)', 'direct')
                  and medium_lc in ('', '(not set)', 'not set', '(none)', 'none')
                  and full_referrer_lc in ('', '(not set)', 'not set')
                    then 'keep_as_clean_direct_candidate'
                else 'still_needs_log_level_review'
            end as clean_direct_reclass_bucket
        from typed
        '''
    )
    summary = conn.execute(
        '''
        select
            clean_direct_reclass_bucket,
            path_group,
            round(sum(sessions), 2) as sessions,
            count(*) as rows
        from v_direct_held_source_referrer_classified
        group by 1, 2
        order by sessions desc nulls last, rows desc
        '''
    ).fetchall()
    summary_csv.parent.mkdir(parents=True, exist_ok=True)
    conn.execute(
        '''
        copy (
            select
                clean_direct_reclass_bucket,
                path_group,
                round(sum(sessions), 2) as sessions,
                count(*) as rows
            from v_direct_held_source_referrer_classified
            group by 1, 2
            order by sessions desc nulls last, rows desc
        ) to ? (header, delimiter ',')
        ''',
        [str(summary_csv)],
    )
    row_count = conn.execute('select count(*) from raw_direct_held_source_referrer_import').fetchone()[0]
    conn.close()
    return row_count, summary


def print_required_columns() -> None:
    print('required_columns')
    for column in REQUIRED_COLUMNS:
        print(column)
    print('optional_columns')
    for column in OPTIONAL_COLUMNS:
        print(column)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Import returned www held Direct source/referrer export and classify clean Direct buckets.'
    )
    parser.add_argument('--input', help='CSV returned by the data team')
    parser.add_argument('--db', default=str(DUCKDB_PATH))
    parser.add_argument('--normalized-output', default=str(NORMALIZED_CSV))
    parser.add_argument('--summary-output', default=str(DEFAULT_SUMMARY))
    parser.add_argument('--print-required-columns', action='store_true')
    args = parser.parse_args()

    if args.print_required_columns:
        print_required_columns()
        return
    if not args.input:
        raise SystemExit('Provide --input or use --print-required-columns')

    input_csv = Path(args.input)
    if not input_csv.exists():
        raise SystemExit(f'Input file not found: {input_csv}')

    rows = read_and_normalize(input_csv)
    try:
        validate_scope(rows)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    normalized_output = Path(args.normalized_output)
    write_normalized(rows, normalized_output)
    row_count, summary = import_to_duckdb(Path(args.db), normalized_output, Path(args.summary_output))

    print(f'normalized_csv={normalized_output}')
    print(f'summary_output={args.summary_output}')
    print(f'imported_rows={row_count}')
    for row in summary:
        print(row)


if __name__ == '__main__':
    main()
