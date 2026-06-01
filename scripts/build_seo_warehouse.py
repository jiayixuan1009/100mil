#!/usr/bin/env python3
import re
from pathlib import Path

import duckdb


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = WORKSPACE_ROOT / 'docs'
WAREHOUSE_DIR = WORKSPACE_ROOT / 'data' / 'warehouse'
DB_PATH = WAREHOUSE_DIR / 'biyapay.duckdb'
PARQUET_DOCS_DIR = WAREHOUSE_DIR / 'parquet' / 'docs'
CATALOG_EXPORT_DIR = WAREHOUSE_DIR / 'catalog_exports'


def table_name_for(path):
    name = re.sub(r'[^a-zA-Z0-9]+', '_', path.stem).strip('_').lower()
    return f'docs_{name}'


def qident(name):
    return '"' + name.replace('"', '""') + '"'


def import_csv(conn, path, table_name):
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
        [str(path)],
    )
    out = PARQUET_DOCS_DIR / f'{table_name}.parquet'
    conn.execute(f'copy {qident(table_name)} to ? (format parquet)', [str(out)])
    count = conn.execute(f'select count(*) from {qident(table_name)}').fetchone()[0]
    return count, out


def import_catalog_exports(conn):
    for filename, table_name in [
        ('raw_files.csv', 'catalog_raw_files'),
        ('workspace_doc_files.csv', 'catalog_workspace_doc_files'),
    ]:
        path = CATALOG_EXPORT_DIR / filename
        if not path.exists():
            continue
        conn.execute(f'drop table if exists {qident(table_name)}')
        conn.execute(
            f'''
            create table {qident(table_name)} as
            select * from read_csv_auto(?, header=true, all_varchar=true, sample_size=-1)
            ''',
            [str(path)],
        )


def create_views(conn, imported_tables):
    if 'docs_phase2_compare_top30_live_health' in imported_tables:
        conn.execute(
            '''
            create or replace view v_compare_blockers as
            select
                url,
                primary_query,
                cast(nullif(impressions, '') as double) as impressions,
                cast(nullif(estimated_click_uplift, '') as double) as estimated_click_uplift,
                status,
                health_class,
                error
            from docs_phase2_compare_top30_live_health
            where health_class = 'technical_blocker' or status like '5%'
            order by impressions desc nulls last
            '''
        )

    if 'docs_phase2_wave1_converter_query_summary' in imported_tables:
        conn.execute(
            '''
            create or replace view v_converter_low_ctr as
            select
                page_key,
                url,
                cast(nullif(clicks, '') as double) as clicks,
                cast(nullif(impressions, '') as double) as impressions,
                cast(nullif(ctr, '') as double) as ctr,
                cast(nullif(avg_position, '') as double) as avg_position,
                top_queries
            from docs_phase2_wave1_converter_query_summary
            order by impressions desc nulls last
            '''
        )

    if 'docs_phase1_gsc_top200_seo_opportunities' in imported_tables:
        conn.execute(
            '''
            create or replace view v_top_gsc_opportunities as
            select
                url,
                page_type,
                primary_query,
                opportunity_class,
                recommended_action,
                priority,
                owner,
                cast(nullif(clicks, '') as double) as clicks,
                cast(nullif(impressions, '') as double) as impressions,
                cast(nullif(ctr, '') as double) as ctr,
                cast(nullif(avg_position, '') as double) as avg_position,
                cast(nullif(estimated_click_uplift, '') as double) as estimated_click_uplift
            from docs_phase1_gsc_top200_seo_opportunities
            order by estimated_click_uplift desc nulls last
            '''
        )

    if 'docs_phase1_top200_technical_status' in imported_tables:
        conn.execute(
            '''
            create or replace view v_technical_p0_p1 as
            select
                url,
                technical_scope,
                status_code,
                indexability,
                title_issue,
                meta_issue,
                h1_issue,
                canonical_issue,
                technical_priority,
                fix_recommendation
            from docs_phase1_top200_technical_status
            where technical_priority in ('P0', 'P1')
            '''
        )

    if 'docs_phase2_wave1_cms_handoff' in imported_tables:
        conn.execute(
            '''
            create or replace view v_wave1_cms_handoff as
            select
                publish_order,
                page_key,
                canonical_url,
                status,
                final_title,
                final_h1,
                primary_cta,
                secondary_cta,
                measurement_key
            from docs_phase2_wave1_cms_handoff
            '''
        )


def main():
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    PARQUET_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(DB_PATH))
    imported = {}

    import_catalog_exports(conn)
    for path in sorted(DOCS_DIR.glob('*.csv')):
        table_name = table_name_for(path)
        count, parquet_path = import_csv(conn, path, table_name)
        imported[table_name] = {'rows': count, 'parquet': str(parquet_path)}

    create_views(conn, set(imported.keys()))
    conn.execute(
        '''
        create or replace view v_workspace_tables as
        select table_name from information_schema.tables
        where table_schema = 'main'
        order by table_name
        '''
    )
    conn.close()

    print(DB_PATH)
    print('imported_doc_csv_tables', len(imported))
    for name, meta in imported.items():
        print(name, meta['rows'])


if __name__ == '__main__':
    main()