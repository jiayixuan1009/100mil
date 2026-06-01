import tempfile
import unittest
from pathlib import Path

import duckdb

from scripts import import_direct_held_source_referrer as direct_import
from scripts import validate_compare_live_urls as compare_live


ROOT = Path(__file__).resolve().parents[1]


class CompareLiveValidationTests(unittest.TestCase):
    def test_noindex_robots_meta_fails_validation(self):
        original_fetch_url = compare_live.fetch_url

        def fake_fetch_url(url, timeout):
            html = (
                '<html><head><title>Compare</title>'
                '<meta name="description" content="Compare rates">'
                '<meta name="robots" content="noindex,nofollow">'
                '<link rel="canonical" href="https://www.biyapay.com/compare/x">'
                '</head><body><h1>Compare rates</h1></body></html>'
            )
            return 200, url, html, '', {'content-type': 'text/html'}, html.encode()

        compare_live.fetch_url = fake_fetch_url
        try:
            result = compare_live.validate_row({'url': 'https://example.com'}, timeout=1)
        finally:
            compare_live.fetch_url = original_fetch_url

        self.assertFalse(result['robots_ok'])
        self.assertEqual(result['health_class'], 'fail')


class DirectHeldImportTests(unittest.TestCase):
    def test_scope_validation_rejects_non_www_or_non_direct_rows(self):
        rows = [
            {
                'date': '2026-01-01',
                'hostname': 'signup.biyapay.com',
                'landing_page_query': '/en/swift',
                'default_channel_group': 'Organic Search',
                'source': 'google',
                'medium': 'organic',
                'full_referrer': '',
                'sessions': '1',
            }
        ]

        with self.assertRaises(ValueError) as ctx:
            direct_import.validate_scope(rows)

        self.assertIn('hostname', str(ctx.exception))
        self.assertIn('default_channel_group', str(ctx.exception))

    def test_has_utm_param_only_matches_literal_utm_prefix(self):
        self.assertTrue(direct_import.has_utm_param('/en/swift?utm_source=google'))
        self.assertTrue(direct_import.has_utm_param('/en/swift?x=1&utm_campaign=spring'))
        self.assertFalse(direct_import.has_utm_param('/en/swift?xutma=1'))
        self.assertFalse(direct_import.has_utm_param('/en/swift?autm_source=wrong'))


class QueryRegressionTests(unittest.TestCase):
    def test_direct_rollup_queries_are_single_statements(self):
        for relative_path in [
            'queries/direct_cleanup_priority_summary.sql',
            'queries/direct_www_content_path_groups.sql',
        ]:
            sql = (ROOT / relative_path).read_text(encoding='utf-8')
            self.assertNotIn(';with ', sql.lower(), relative_path)
            self.assertEqual(sql.count(';'), 1, relative_path)

    def test_direct_query_signal_sql_does_not_misclassify_xutma_as_utm(self):
        conn = duckdb.connect(':memory:')
        conn.execute(
            """
            create table v_raw_ga4_page_location_events (
                hostname varchar,
                page_location varchar,
                sessions double,
                active_users double
            )
            """
        )
        conn.execute(
            """
            insert into v_raw_ga4_page_location_events values
            ('www.biyapay.com', 'https://www.biyapay.com/en/swift?xutma=1', 10, 9)
            """
        )
        rows = conn.execute(
            (ROOT / 'queries/direct_www_query_signal_summary.sql').read_text(encoding='utf-8')
        ).fetchall()
        conn.close()

        self.assertEqual(rows, [('other_query_params', 10.0, 9.0, 1)])


class RawImportManifestTests(unittest.TestCase):
    def test_manifest_records_partial_import_when_rows_are_skipped(self):
        from scripts import ingest_selected_raw_sources as raw_import

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / 'bad.csv'
            csv_path.write_bytes(b'a,b\n1,2\n\xff,3\n')
            conn = duckdb.connect(':memory:')
            raw_import.ensure_manifest(conn)

            row = {
                'relative_path': 'ga4/bad.csv',
                'absolute_path': str(csv_path),
                'file_name': 'bad.csv',
                'size_bytes': csv_path.stat().st_size,
                'line_count': 3,
            }
            status, *_ = raw_import.import_one(conn, row)
            manifest = conn.execute(
                'select import_status, expected_data_rows, skipped_rows from raw_import_manifest'
            ).fetchone()
            conn.close()

        self.assertEqual(status, 'partial')
        self.assertEqual(manifest, ('partial', 2, 1))


if __name__ == '__main__':
    unittest.main()
