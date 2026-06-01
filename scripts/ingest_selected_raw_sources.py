#!/usr/bin/env python3
import argparse
import hashlib
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import duckdb


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_DIR = WORKSPACE_ROOT / 'data' / 'warehouse'
CATALOG_DB = WAREHOUSE_DIR / 'catalog.sqlite'
DUCKDB_PATH = WAREHOUSE_DIR / 'biyapay.duckdb'
RAW_PARQUET_DIR = WAREHOUSE_DIR / 'parquet' / 'raw_selected'
DEFAULT_MAX_MB = 60
KEYWORDS = (
    'gsc',
    'ga4',
    'cross',
    'ai-search',
    'hostname',
    'mapping',
    'indexability',
    'orphan',
)


def qident(name):
    return '"' + name.replace('"', '""') + '"'


def table_name_for(relative_path):
    base = re.sub(r'[^a-zA-Z0-9]+', '_', relative_path).strip('_').lower()
    digest = hashlib.sha1(relative_path.encode('utf-8')).hexdigest()[:8]
    return f'raw_{base[:72]}_{digest}'


def source_group(relative_path):
    lowered = relative_path.lower()
    if 'gsc' in lowered:
        return 'gsc'
    if 'ga4' in lowered or '/ga/' in lowered:
        return 'ga4'
    if 'cross' in lowered or 'mapping' in lowered:
        return 'cross_domain'
    if 'ai-search' in lowered:
        return 'ai_search'
    if 'indexability' in lowered or 'orphan' in lowered or '/sf/' in lowered:
        return 'technical_seo'
    return 'other'


def load_candidates(max_mb):
    max_bytes = max_mb * 1024 * 1024
    conn = sqlite3.connect(CATALOG_DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        '''
        select absolute_path, relative_path, file_name, size_bytes, line_count, header_json
        from file_catalog
        where source_scope = 'raw_backup'
          and ingest_strategy = 'duckdb_import_now'
          and extension like '%.csv'
          and size_bytes <= ?
        order by size_bytes desc
        ''',
        [max_bytes],
    ).fetchall()
    conn.close()
    selected = []
    for row in rows:
        relative_path = row['relative_path']
        lowered = relative_path.lower()
        if any(keyword in lowered for keyword in KEYWORDS):
            selected.append(dict(row))
    return selected


def ensure_manifest(conn):
    conn.execute(
        '''
        create table if not exists raw_import_manifest (
            table_name varchar,
            source_group varchar,
            relative_path varchar,
            absolute_path varchar,
            file_name varchar,
            size_bytes bigint,
            line_count varchar,
            expected_data_rows bigint,
            imported_rows bigint,
            skipped_rows bigint,
            parquet_path varchar,
            import_status varchar,
            error varchar,
            imported_at_utc varchar
        )
        '''
    )
    existing_columns = {
        row[1]
        for row in conn.execute("pragma table_info('raw_import_manifest')").fetchall()
    }
    if 'expected_data_rows' not in existing_columns:
        conn.execute('alter table raw_import_manifest add column expected_data_rows bigint')
    if 'skipped_rows' not in existing_columns:
        conn.execute('alter table raw_import_manifest add column skipped_rows bigint')
    conn.execute('delete from raw_import_manifest')


def expected_rows_from_line_count(line_count):
    try:
        value = int(line_count)
    except (TypeError, ValueError):
        return None
    return max(value - 1, 0)


def import_one(conn, row):
    relative_path = row['relative_path']
    table_name = table_name_for(relative_path)
    parquet_path = RAW_PARQUET_DIR / f'{table_name}.parquet'
    imported_at = datetime.now(timezone.utc).isoformat()
    expected_data_rows = expected_rows_from_line_count(row.get('line_count'))
    try:
        conn.execute(f'drop table if exists {qident(table_name)}')
        conn.execute(
            f'''
            create table {qident(table_name)} as
            select * from read_csv_auto(
                ?,
                header=true,
                all_varchar=true,
                ignore_errors=true,
                sample_size=-1
            )
            ''',
            [row['absolute_path']],
        )
        imported_rows = conn.execute(f'select count(*) from {qident(table_name)}').fetchone()[0]
        conn.execute(f'copy {qident(table_name)} to ? (format parquet)', [str(parquet_path)])
        skipped_rows = (
            max(expected_data_rows - imported_rows, 0)
            if expected_data_rows is not None
            else None
        )
        status = 'partial' if skipped_rows else 'imported'
        error = ''
    except Exception as exc:
        imported_rows = 0
        skipped_rows = expected_data_rows
        status = 'failed'
        error = f'{exc.__class__.__name__}: {exc}'[:500]
    conn.execute(
        '''
        insert into raw_import_manifest (
            table_name,
            source_group,
            relative_path,
            absolute_path,
            file_name,
            size_bytes,
            line_count,
            expected_data_rows,
            imported_rows,
            skipped_rows,
            parquet_path,
            import_status,
            error,
            imported_at_utc
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        [
            table_name,
            source_group(relative_path),
            relative_path,
            row['absolute_path'],
            row['file_name'],
            row['size_bytes'],
            str(row['line_count'] or ''),
            expected_data_rows,
            imported_rows,
            skipped_rows,
            str(parquet_path) if status in ('imported', 'partial') else '',
            status,
            error,
            imported_at,
        ],
    )
    return status, table_name, imported_rows, relative_path, error


def create_views(conn):
    conn.execute(
        '''
        create or replace view v_raw_source_inventory as
        select
            source_group,
            count(*) as files,
            round(sum(size_bytes) / 1024.0 / 1024.0, 2) as size_mb,
            sum(imported_rows) as imported_rows,
            sum(case when import_status = 'imported' then 1 else 0 end) as imported_files,
            sum(case when import_status = 'partial' then 1 else 0 end) as partial_files,
            sum(case when import_status = 'failed' then 1 else 0 end) as failed_files
        from raw_import_manifest
        group by source_group
        order by size_mb desc
        '''
    )
    conn.execute(
        '''
        create or replace view v_raw_import_failures as
        select table_name, source_group, relative_path, import_status, skipped_rows, error
        from raw_import_manifest
        where import_status in ('failed', 'partial')
        order by source_group, relative_path
        '''
    )
    conn.execute(
        '''
        create or replace view v_raw_imported_tables as
        select table_name, source_group, relative_path, imported_rows, round(size_bytes / 1024.0 / 1024.0, 2) as size_mb
        from raw_import_manifest
        where import_status in ('imported', 'partial')
        order by source_group, size_bytes desc
        '''
    )

    manifest = dict(conn.execute("select relative_path, table_name from raw_import_manifest where import_status in ('imported', 'partial')").fetchall())

    def table_for(relative_path):
        table_name = manifest.get(relative_path)
        return qident(table_name) if table_name else None

    hostname_table = table_for('5-22/ga4_hostname_audit_28d_2026-04-24_to_2026-05-21.csv')
    if hostname_table:
        conn.execute(
            f'''
            create or replace view v_raw_ga4_hostname_audit as
            select
                "操作系统" as operating_system,
                "主机名" as hostname,
                cast(nullif("活跃用户", '') as double) as active_users,
                cast(nullif("新用户数", '') as double) as new_users,
                cast(nullif("感兴趣的会话数", '') as double) as engaged_sessions,
                cast(nullif("感兴趣的会话占比", '') as double) as engagement_rate,
                cast(nullif("事件数", '') as double) as event_count,
                cast(nullif("关键事件数", '') as double) as key_events,
                case
                    when "主机名" in ('www.biyapay.com', 'biyapay.com', 'cn.biyapay.com') then 'core'
                    when "主机名" like '%.biyapay.com' then 'subdomain'
                    else 'pollution_or_external'
                end as hostname_class
            from {hostname_table}
            order by active_users desc nulls last
            '''
        )

    page_location_table = table_for('ga4/ga4_page_location_pii_token_check_2025-11-20_2026-05-19.csv')
    if page_location_table:
        conn.execute(
            f'''
            create or replace view v_raw_ga4_page_location_events as
            select
                "主机名" as hostname,
                "网页路径 + 查询字符串" as page_path_query,
                "网页位置" as page_location,
                "事件名称" as event_name,
                cast(nullif("事件数", '') as double) as event_count,
                cast(nullif("活跃用户", '') as double) as active_users,
                cast(nullif("会话数", '') as double) as sessions,
                case
                    when lower("网页位置") like '%token%' or lower("网页位置") like '%code=%' or lower("网页位置") like '%email%' then 'possible_sensitive_url'
                    when "主机名" not in ('www.biyapay.com', 'biyapay.com', 'cn.biyapay.com') then 'non_core_hostname'
                    else 'normal'
                end as audit_flag
            from {page_location_table}
            order by sessions desc nulls last
            '''
        )

    cross_stock_table = table_for('cross/invest_www_stock_url_mapping_2026-05-22.csv')
    if cross_stock_table:
        conn.execute(
            f'''
            create or replace view v_raw_cross_stock_mapping as
            select
                url,
                host,
                locale,
                category,
                ticker_or_slug,
                ticker_canonical_form,
                cast(nullif(gsc_clicks_16m, '') as double) as gsc_clicks_16m,
                cast(nullif(gsc_impressions_16m, '') as double) as gsc_impressions_16m,
                cast(nullif(gsc_ctr_pct, '') as double) as gsc_ctr_pct,
                cast(nullif(gsc_position, '') as double) as gsc_position,
                status_code,
                indexability,
                sf_title,
                overlap_with_other_host,
                recommend_d2_action,
                data_source,
                notes
            from {cross_stock_table}
            order by gsc_impressions_16m desc nulls last
            '''
        )

    ai_table = table_for('ai-search/baseline_2026-04-26.csv')
    if ai_table:
        conn.execute(
            f'''
            create or replace view v_raw_ai_search_baseline as
            select
                query_id,
                category,
                keyword,
                query_text,
                channel,
                test_date,
                cited_biyapay,
                cast(nullif(biyapay_position, '') as double) as biyapay_position,
                biyapay_url,
                biyapay_snippet,
                competitors_cited,
                response_file,
                notes
            from {ai_table}
            order by category, channel, query_id
            '''
        )

    orphan_table = table_for('01 www/sf/0518 orphan_pages.csv')
    if orphan_table:
        conn.execute(
            f'''
            create or replace view v_raw_www_orphan_pages_0518 as
            select
                URL as url,
                Source as source,
                case
                    when lower(URL) like '%/converter/%' then 'converter'
                    when lower(URL) like '%/compare/%' then 'compare'
                    when lower(URL) like '%/blogdetail/%' then 'blogdetail'
                    when lower(URL) like '%/stock/%' or lower(URL) like '%/us-stock/%' then 'stock'
                    else 'other'
                end as page_type_guess
            from {orphan_table}
            '''
        )


def main():
    parser = argparse.ArgumentParser(description='Import selected high-value raw CSV sources into DuckDB.')
    parser.add_argument('--max-mb', type=int, default=DEFAULT_MAX_MB)
    args = parser.parse_args()

    RAW_PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    candidates = load_candidates(args.max_mb)
    conn = duckdb.connect(str(DUCKDB_PATH))
    ensure_manifest(conn)

    imported = 0
    failed = 0
    for row in candidates:
        status, table_name, imported_rows, relative_path, error = import_one(conn, row)
        if status in ('imported', 'partial'):
            imported += 1
            print('imported', table_name, imported_rows, relative_path)
        else:
            failed += 1
            print('failed', table_name, relative_path, error)

    create_views(conn)
    conn.close()
    print('selected_candidates', len(candidates), 'imported', imported, 'failed', failed)


if __name__ == '__main__':
    main()
