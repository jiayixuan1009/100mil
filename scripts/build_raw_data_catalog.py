#!/usr/bin/env python3
import argparse
import csv
import gzip
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


RAW_ROOT = Path('/Volumes/SSD/Backups/来自：INTEL admin 电脑备份/seoaudition/data/raw')
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_DIR = WORKSPACE_ROOT / 'data' / 'warehouse'
CATALOG_DB = WAREHOUSE_DIR / 'catalog.sqlite'
EXPORT_DIR = WAREHOUSE_DIR / 'catalog_exports'
LINE_COUNT_MAX_BYTES = 250 * 1024 * 1024


def iso_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def is_text_like(path):
    return path.suffix.lower() in {'.csv', '.tsv', '.txt', '.md', '.json', '.sql', '.log'} or path.name.endswith('.csv.gz')


def read_header(path):
    try:
        if path.name.endswith('.csv.gz'):
            opener = lambda p: gzip.open(p, 'rt', encoding='utf-8-sig', errors='replace', newline='')
        else:
            opener = lambda p: open(p, 'r', encoding='utf-8-sig', errors='replace', newline='')
        with opener(path) as handle:
            if path.suffix.lower() in {'.csv', '.tsv'} or path.name.endswith('.csv.gz'):
                delimiter = '\t' if path.suffix.lower() == '.tsv' else ','
                return next(csv.reader(handle, delimiter=delimiter), [])
            first_line = handle.readline().strip()
            return [first_line[:240]] if first_line else []
    except Exception as exc:
        return [f'HEADER_READ_ERROR: {exc.__class__.__name__}']


def count_lines_if_safe(path, size_bytes):
    if not is_text_like(path):
        return None, 'skipped_non_text'
    if size_bytes > LINE_COUNT_MAX_BYTES:
        return None, 'skipped_large_file'
    try:
        if path.name.endswith('.gz'):
            with gzip.open(path, 'rb') as handle:
                return sum(1 for _ in handle), 'counted'
        with open(path, 'rb') as handle:
            return sum(1 for _ in handle), 'counted'
    except Exception as exc:
        return None, f'count_error:{exc.__class__.__name__}'


def file_record(path, root, source_scope):
    stat = path.stat()
    line_count, line_count_status = count_lines_if_safe(path, stat.st_size)
    header = read_header(path) if is_text_like(path) and stat.st_size <= LINE_COUNT_MAX_BYTES else []
    return {
        'source_scope': source_scope,
        'absolute_path': str(path),
        'relative_path': str(path.relative_to(root)),
        'file_name': path.name,
        'extension': ''.join(path.suffixes).lower() or path.suffix.lower(),
        'size_bytes': stat.st_size,
        'modified_at_utc': iso_from_timestamp(stat.st_mtime),
        'line_count': line_count,
        'line_count_status': line_count_status,
        'header_json': json.dumps(header, ensure_ascii=False),
        'ingest_strategy': ingest_strategy(path, stat.st_size),
        'cataloged_at_utc': datetime.now(timezone.utc).isoformat(),
    }


def ingest_strategy(path, size_bytes):
    suffix = path.suffix.lower()
    if path.name.endswith('.csv.gz'):
        return 'duckdb_read_csv_gzip_if_needed'
    if suffix == '.csv' and size_bytes <= 500 * 1024 * 1024:
        return 'duckdb_import_now'
    if suffix == '.csv':
        return 'stream_filter_before_import'
    if suffix in {'.xlsx', '.zip', '.docx', '.png'}:
        return 'catalog_only'
    if suffix in {'.md', '.txt', '.json', '.sql', '.log'}:
        return 'catalog_and_read_on_demand'
    return 'catalog_only'


def scan_files(root, source_scope):
    if not root.exists():
        return []
    rows = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.is_file():
                rows.append(file_record(path, root, source_scope))
    return rows


def write_sqlite(rows):
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CATALOG_DB)
    conn.execute('drop table if exists file_catalog')
    conn.execute(
        '''
        create table file_catalog (
            source_scope text,
            absolute_path text primary key,
            relative_path text,
            file_name text,
            extension text,
            size_bytes integer,
            modified_at_utc text,
            line_count integer,
            line_count_status text,
            header_json text,
            ingest_strategy text,
            cataloged_at_utc text
        )
        '''
    )
    conn.executemany(
        '''
        insert into file_catalog values (
            :source_scope, :absolute_path, :relative_path, :file_name, :extension,
            :size_bytes, :modified_at_utc, :line_count, :line_count_status,
            :header_json, :ingest_strategy, :cataloged_at_utc
        )
        ''',
        rows,
    )
    conn.execute('create index idx_file_catalog_scope on file_catalog(source_scope)')
    conn.execute('create index idx_file_catalog_extension on file_catalog(extension)')
    conn.execute('create index idx_file_catalog_strategy on file_catalog(ingest_strategy)')
    conn.commit()
    conn.close()


def write_csv_export(rows, filename):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = EXPORT_DIR / filename
    fields = [
        'source_scope', 'absolute_path', 'relative_path', 'file_name', 'extension',
        'size_bytes', 'modified_at_utc', 'line_count', 'line_count_status',
        'header_json', 'ingest_strategy', 'cataloged_at_utc'
    ]
    with out.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return out


def main():
    parser = argparse.ArgumentParser(description='Build a SQLite file catalog for BiyaPay raw SEO data.')
    parser.add_argument('--raw-root', default=str(RAW_ROOT))
    parser.add_argument('--workspace-root', default=str(WORKSPACE_ROOT))
    args = parser.parse_args()

    raw_root = Path(args.raw_root)
    workspace_root = Path(args.workspace_root)
    raw_rows = scan_files(raw_root, 'raw_backup')
    docs_rows = scan_files(workspace_root / 'docs', 'workspace_docs')
    rows = raw_rows + docs_rows

    write_sqlite(rows)
    raw_export = write_csv_export(raw_rows, 'raw_files.csv')
    docs_export = write_csv_export(docs_rows, 'workspace_doc_files.csv')

    print(CATALOG_DB)
    print(raw_export)
    print(docs_export)
    print('rows', len(rows), 'raw', len(raw_rows), 'workspace_docs', len(docs_rows))


if __name__ == '__main__':
    main()