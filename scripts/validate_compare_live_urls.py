#!/usr/bin/env python3
import argparse
import csv
import hashlib
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE_ROOT / 'docs' / 'phase2_compare_p0_fix_acceptance.csv'
DEFAULT_OUTPUT = WORKSPACE_ROOT / 'docs' / 'phase3_compare_live_regression_current.csv'


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.meta_description = ''
        self.canonical = ''
        self.robots = ''
        self.h1 = ''
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = {key.lower(): value for key, value in attrs if key}
        lower_tag = tag.lower()
        if lower_tag == 'title':
            self._in_title = True
        elif lower_tag == 'h1':
            self._in_h1 = True
        elif lower_tag == 'meta':
            name = (attrs_dict.get('name') or attrs_dict.get('property') or '').lower()
            content = attrs_dict.get('content') or ''
            if name == 'description' and not self.meta_description:
                self.meta_description = content.strip()
            elif name == 'robots' and not self.robots:
                self.robots = content.strip()
        elif lower_tag == 'link':
            rel = (attrs_dict.get('rel') or '').lower()
            if 'canonical' in rel and not self.canonical:
                self.canonical = (attrs_dict.get('href') or '').strip()

    def handle_endtag(self, tag):
        lower_tag = tag.lower()
        if lower_tag == 'title':
            self._in_title = False
        elif lower_tag == 'h1':
            self._in_h1 = False

    def handle_data(self, data):
        text = re.sub(r'\s+', ' ', data).strip()
        if not text:
            return
        if self._in_title and not self.title:
            self.title = text
        elif self._in_h1 and not self.h1:
            self.h1 = text


def fetch_url(url, timeout):
    request = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; BiyaPaySEORegression/1.0; +https://www.biyapay.com/)'
    })
    context = ssl.create_default_context()
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            status = response.getcode()
            final_url = response.geturl()
            content_type = response.headers.get('content-type', '')
            body = response.read(700_000)
            html = body.decode('utf-8', errors='replace') if 'html' in content_type.lower() or body else ''
            return status, final_url, html, '', response.headers, body
    except HTTPError as exc:
        body = exc.read(300_000)
        html = body.decode('utf-8', errors='replace') if body else ''
        return exc.code, exc.geturl(), html, str(exc.reason or exc), exc.headers, body
    except URLError as exc:
        return 0, url, '', str(exc.reason or exc), {}, b''
    except Exception as exc:
        return 0, url, '', f'{exc.__class__.__name__}: {exc}', {}, b''


def robots_allows_index(robots):
    if not robots:
        return False
    tokens = {
        token.strip().lower()
        for token in re.split(r'[,;\s]+', robots)
        if token.strip()
    }
    return 'noindex' not in tokens and ('index' in tokens or 'all' in tokens)


def validate_row(row, timeout):
    url = row['url']
    status, final_url, html, error, headers, body = fetch_url(url, timeout)
    parser = MetaParser()
    if html:
        parser.feed(html)
    title = parser.title
    meta = parser.meta_description
    canonical = parser.canonical
    robots = parser.robots
    h1 = parser.h1

    checks = {
        'status_ok': status == 200,
        'title_ok': bool(title),
        'meta_ok': bool(meta),
        'canonical_ok': bool(canonical),
        'robots_ok': robots_allows_index(robots),
        'h1_ok': bool(h1),
    }
    health_class = 'pass' if all(checks.values()) else 'fail'
    body_preview = re.sub(r'\s+', ' ', html).strip()[:180]
    return {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'priority': row.get('priority', ''),
        'url': url,
        'primary_query': row.get('primary_query', ''),
        'impressions': row.get('impressions', ''),
        'avg_position': row.get('avg_position', ''),
        'status': status,
        'final_url': final_url,
        'content_type': headers.get('content-type', '') if headers else '',
        'server': headers.get('server', '') if headers else '',
        'x_powered_by': headers.get('x-powered-by', '') if headers else '',
        'cache_control': headers.get('cache-control', '') if headers else '',
        'body_bytes': len(body),
        'body_sha256': hashlib.sha256(body).hexdigest() if body else '',
        'body_preview': body_preview,
        'title': title,
        'title_length': len(title),
        'meta_description': meta,
        'meta_length': len(meta),
        'h1': h1,
        'h1_length': len(h1),
        'canonical': canonical,
        'robots': robots,
        'status_ok': checks['status_ok'],
        'title_ok': checks['title_ok'],
        'meta_ok': checks['meta_ok'],
        'canonical_ok': checks['canonical_ok'],
        'robots_ok': checks['robots_ok'],
        'h1_ok': checks['h1_ok'],
        'health_class': health_class,
        'error': error,
    }


def main():
    parser = argparse.ArgumentParser(description='Validate live compare P0 URLs after engineering fixes.')
    parser.add_argument('--input', default=str(DEFAULT_INPUT))
    parser.add_argument('--output', default=str(DEFAULT_OUTPUT))
    parser.add_argument('--timeout', type=int, default=20)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    rows = list(csv.DictReader(input_path.open('r', encoding='utf-8-sig', newline='')))
    results = [validate_row(row, args.timeout) for row in rows]
    fields = list(results[0].keys()) if results else []
    with output_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    passed = sum(1 for row in results if row['health_class'] == 'pass')
    failed = len(results) - passed
    print(output_path)
    print('checked', len(results), 'passed', passed, 'failed', failed)


if __name__ == '__main__':
    main()
