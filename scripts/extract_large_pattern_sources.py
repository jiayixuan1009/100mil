#!/usr/bin/env python3
import argparse
import csv
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
EXTRACT_DIR = WAREHOUSE_DIR / 'extracts' / 'large_patterns'
PARQUET_DIR = WAREHOUSE_DIR / 'parquet' / 'large_patterns'

DEFAULT_PATTERNS = {
    'compare': ['/compare/'],
    'converter': ['/converter/'],
    'blogdetail': ['/blogdetail/', '/blogDetail/'],
    'stock': ['/stock/', '/us-stock/', '/hk-stock/'],
    'iban': ['/iban'],
    'swift': ['/swift'],
    'sendmoney': ['/sendmoney'],
    'download': ['/download'],
}

DEFAULT_SOURCES = [
    '01 www/sf/0518 all_inlinks.csv',
    '01 www/sf/0518 contains_structured_data_detailed_report.csv',
    '01 www/sf/0513 response_codes_all.csv',
    '01 www/sf/0518 internal_all.csv',
    '01 www/sf/0513 internal_all.csv',
    '01 www/gsc/api_cube_2026-05-22/query_date_api_rows.csv',
]


def qident(name):
    return '"' + name.replace('"', '""') + '"'


def slug_for(relative_path):
    base = re.sub(r'[^a-zA-Z0-9]+', '_', relative_path).strip('_').lower()
    digest = hashlib.sha1(relative_path.encode('utf-8')).hexdigest()[:8]
    return f'{base[:72]}_{digest}'


def source_kind(relative_path):
    lower = relative_path.lower()
    if 'all_inlinks' in lower:
        return 'inlinks'
    if 'structured_data' in lower:
        return 'structured_data'
    if 'response_codes' in lower:
        return 'response_codes'
    if 'internal_all' in lower:
        return 'internal_all'
    if 'query_date_api_rows' in lower:
        return 'gsc_query_date'
    return 'other'


def load_source_paths(relative_paths):
    conn = sqlite3.connect(CATALOG_DB)
    conn.row_factory = sqlite3.Row
    placeholders = ','.join('?' for _ in relative_paths)
    rows = conn.execute(
        f'''
        select relative_path, absolute_path, size_bytes
        from file_catalog
        where source_scope = 'raw_backup'
          and relative_path in ({placeholders})
        order by size_bytes desc
        ''',
        relative_paths,
    ).fetchall()
    conn.close()
    found = {row['relative_path']: dict(row) for row in rows}
    missing = [path for path in relative_paths if path not in found]
    if missing:
        raise SystemExit(f'Missing source files in catalog: {missing}')
    return [found[path] for path in relative_paths]


def parse_header(line):
    return next(csv.reader([line]))


def matched_pattern_keys(text, patterns_map):
    lower_text = text.lower()
    keys = []
    for key, patterns in patterns_map.items():
        if any(pattern.lower() in lower_text for pattern in patterns):
            keys.append(key)
    return keys


def match_column_names(kind, header):
    wanted_by_kind = {
        'inlinks': {'Source', 'Destination'},
        'structured_data': {'URL', 'Subject', 'Object'},
        'response_codes': {'Address', 'Redirect URL'},
        'internal_all': {'Address', 'Redirect URL', 'Canonical Link Element 1'},
        'gsc_query_date': {'page_filter', 'api_row_json'},
    }
    wanted = wanted_by_kind.get(kind, set(header))
    return [index for index, column in enumerate(header) if column in wanted]


def extract_source(source, patterns_map, max_rows_per_source=None, progress_every=5_000_000):
    relative_path = source['relative_path']
    absolute_path = Path(source['absolute_path'])
    slug = slug_for(relative_path)
    out_path = EXTRACT_DIR / f'{slug}.csv'
    scanned = 0
    matched = 0
    malformed = 0
    started_at = datetime.now(timezone.utc).isoformat()

    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    kind = source_kind(relative_path)
    with absolute_path.open('r', encoding='utf-8-sig', errors='replace', newline='') as input_handle:
        reader = csv.reader(input_handle)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f'Empty source file: {absolute_path}')
        match_columns = match_column_names(kind, header)
        output_header = ['source_relative_path', 'source_kind', 'matched_patterns'] + header
        with out_path.open('w', encoding='utf-8', newline='') as output_handle:
            writer = csv.writer(output_handle)
            writer.writerow(output_header)
            for row in reader:
                scanned += 1
                match_text = ' '.join(row[index] for index in match_columns if index < len(row))
                pattern_keys = matched_pattern_keys(match_text, patterns_map)
                if not pattern_keys:
                    if progress_every and scanned % progress_every == 0:
                        print('progress', relative_path, 'scanned', scanned, 'matched', matched, flush=True)
                    continue
                if len(row) < len(header):
                    row = row + [''] * (len(header) - len(row))
                elif len(row) > len(header):
                    row = row[:len(header)]
                writer.writerow([relative_path, source_kind(relative_path), '|'.join(pattern_keys)] + row)
                matched += 1
                if max_rows_per_source and matched >= max_rows_per_source:
                    break
                if progress_every and scanned % progress_every == 0:
                    print('progress', relative_path, 'scanned', scanned, 'matched', matched, flush=True)

    return {
        'relative_path': relative_path,
        'absolute_path': str(absolute_path),
        'source_kind': source_kind(relative_path),
        'extract_path': str(out_path),
        'scanned_rows': scanned,
        'matched_rows': matched,
        'malformed_rows': malformed,
        'started_at_utc': started_at,
        'finished_at_utc': datetime.now(timezone.utc).isoformat(),
    }


def import_extracts(results):
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(DUCKDB_PATH))
    conn.execute(
        '''
        create table if not exists large_pattern_extract_manifest (
            table_name varchar,
            relative_path varchar,
            absolute_path varchar,
            source_kind varchar,
            extract_path varchar,
            parquet_path varchar,
            scanned_rows bigint,
            matched_rows bigint,
            malformed_rows bigint,
            imported_rows bigint,
            started_at_utc varchar,
            finished_at_utc varchar,
            imported_at_utc varchar
        )
        '''
    )
    conn.execute('delete from large_pattern_extract_manifest')
    for result in results:
        table_name = f'large_{source_kind(result["relative_path"])}_{slug_for(result["relative_path"])}'
        extract_path = Path(result['extract_path'])
        parquet_path = PARQUET_DIR / f'{table_name}.parquet'
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
            [str(extract_path)],
        )
        imported_rows = conn.execute(f'select count(*) from {qident(table_name)}').fetchone()[0]
        conn.execute(f'copy {qident(table_name)} to ? (format parquet)', [str(parquet_path)])
        conn.execute(
            '''
            insert into large_pattern_extract_manifest values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            [
                table_name,
                result['relative_path'],
                result['absolute_path'],
                result['source_kind'],
                result['extract_path'],
                str(parquet_path),
                result['scanned_rows'],
                result['matched_rows'],
                result['malformed_rows'],
                imported_rows,
                result['started_at_utc'],
                result['finished_at_utc'],
                datetime.now(timezone.utc).isoformat(),
            ],
        )
        print('imported_extract', table_name, 'rows', imported_rows, flush=True)
    create_views(conn)
    conn.close()


def create_views(conn):
    conn.execute(
        '''
        create or replace view v_large_pattern_extract_inventory as
        select
            source_kind,
            relative_path,
            table_name,
            scanned_rows,
            matched_rows,
            malformed_rows,
            imported_rows,
            extract_path,
            parquet_path
        from large_pattern_extract_manifest
        order by matched_rows desc
        '''
    )

    manifest = conn.execute('select source_kind, table_name from large_pattern_extract_manifest').fetchall()
    for kind in ['inlinks', 'structured_data', 'response_codes', 'internal_all', 'gsc_query_date']:
        tables = [qident(table_name) for source_kind_value, table_name in manifest if source_kind_value == kind]
        view_name = f'v_large_pattern_{kind}'
        if not tables:
            continue
        union_sql = '\nunion all by name\n'.join(f'select * from {table}' for table in tables)
        conn.execute(f'create or replace view {qident(view_name)} as {union_sql}')

    summary_parts = []
    for kind in ['inlinks', 'structured_data', 'response_codes', 'internal_all', 'gsc_query_date']:
        if any(source_kind_value == kind for source_kind_value, _ in manifest):
            summary_parts.append(f'select source_kind, matched_patterns from {qident(f"v_large_pattern_{kind}")}')
    if summary_parts:
        conn.execute(
            f'''
            create or replace view v_large_pattern_summary as
            select
                source_kind,
                matched_patterns,
                count(*) as rows
            from (
                {' union all '.join(summary_parts)}
            )
            group by source_kind, matched_patterns
            order by rows desc
            '''
        )


def main():
    parser = argparse.ArgumentParser(description='Stream-extract URL-pattern subsets from huge raw CSVs and import them into DuckDB.')
    parser.add_argument('--source', action='append', choices=['all', 'inlinks', 'structured_data', 'response_codes', 'internal_all', 'gsc_query_date'], default=[])
    parser.add_argument('--pattern', action='append', choices=['all'] + sorted(DEFAULT_PATTERNS), default=[])
    parser.add_argument('--max-rows-per-source', type=int, default=None)
    parser.add_argument('--progress-every', type=int, default=5_000_000)
    args = parser.parse_args()

    selected_kinds = set(args.source or ['all'])
    selected_patterns = set(args.pattern or ['all'])
    patterns_map = DEFAULT_PATTERNS if 'all' in selected_patterns else {key: DEFAULT_PATTERNS[key] for key in selected_patterns}
    sources = load_source_paths(DEFAULT_SOURCES)
    if 'all' not in selected_kinds:
        sources = [source for source in sources if source_kind(source['relative_path']) in selected_kinds]

    results = []
    for source in sources:
        print('extracting', source['relative_path'], flush=True)
        result = extract_source(source, patterns_map, max_rows_per_source=args.max_rows_per_source, progress_every=args.progress_every)
        print('extracted', result['relative_path'], 'scanned', result['scanned_rows'], 'matched', result['matched_rows'], 'malformed', result['malformed_rows'], flush=True)
        results.append(result)

    import_extracts(results)
    print('sources', len(results), 'matched_rows', sum(result['matched_rows'] for result in results), flush=True)


if __name__ == '__main__':
    main()