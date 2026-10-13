"""Read-only Canadian starter-laptop comparison. No shopping account or purchase.

Run: python laptop_finder.py --output results/laptops.json
Only exact configurations on the two manufacturers' new-laptop pages are ranked.
If a page changes or cannot be verified, it contributes no candidate.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import threading
import time
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

SOURCES = (
    ('Dell Canada', 'https://www.dell.com/en-ca/shop/deals/pc-laptop-deals'),
    ('HP Canada', 'https://www.hp.com/ca-en/shop/listings/laptops?memstd=16-gb&cap=512-gb'),
)
HOSTS = {'www.dell.com', 'www.hp.com'}
MAX_BYTES = 6_000_000
_lock = threading.Lock()
_cache = None
_expires = 0


def safe_url(url):
    p = urlparse(url)
    return p.scheme == 'https' and p.hostname in HOSTS and p.port in (None, 443) and not p.username and not p.password


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not safe_url(newurl):
            raise ValueError('Store redirected outside the checked manufacturers')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    if not safe_url(url):
        raise ValueError('Unsupported store')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; StepstoneLaptopFinder/1.0)', 'Accept': 'text/html'})
    with build_opener(SafeRedirect()).open(req, timeout=12) as response:
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('Store page exceeded the comparison limit')
        return raw.decode('utf-8', errors='replace')


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.attrs = []
    def handle_starttag(self, tag, attrs):
        self.attrs.append((tag, dict(attrs)))
    def handle_data(self, data):
        self.parts.append(data)


def plain(source):
    p = Text()
    p.feed(source)
    return re.sub(r'\s+', ' ', ' '.join(p.parts)).strip()


def cents(text):
    try:
        value = Decimal(re.sub(r'[^\d.]', '', text))
        if not value.is_finite() or value <= 0 or value > 20_000:
            return None
        return int(value * 100)
    except InvalidOperation:
        return None


def comparable_processor(text):
    text = re.sub(r'[®™]', '', text).lower()
    text = re.sub(r'\s+', ' ', text)
    # Conservative compatibility and generation floor, not a benchmark claim.
    if re.search(r'core (?:ultra )?[579]\s*[-:]?\s*[123]\d{2}[uhv]?\b', text):
        return True
    for grade, model in re.findall(r'\bi([579])(?:\s*-\s*|\s+)(\d{4,5})[a-z]*', text):
        # Mobile 12th–14th generation parts also use four digits (i5-1235U).
        generation = int(model[:2]) if len(model) == 5 or int(model[:2]) in (12, 13, 14, 15) else int(model[0])
        if generation >= 12:
            return True
    if re.search(r'ryzen ai [579]', text):
        return True
    for grade, model in re.findall(r'ryzen ([579])\s*[-:]?\s*(\d{3,4})[a-z]*', text):
        n = int(model)
        if (len(model) == 3 and n >= 200) or (n >= 5500 and n not in (7520, 7320)):
            return True
    return False


def qualify(item):
    title = item['title']
    specs = item['specs']
    text = ' '.join(specs)
    if not safe_url(item['url']) or re.search(r'refurb|renewed|recertified|open[- ]?box|pre[- ]?owned|used\b|outlet', title + ' ' + item['url'], re.I):
        return None
    if not item.get('inStock') or not item.get('priceCents') or not comparable_processor(text):
        return None
    hardware = re.sub(r'[,;:]', ' ', text)
    hardware = re.sub(r'\bM\.2\b', ' ', hardware, flags=re.I)
    ram = re.search(r'\b(\d+)\s*GB\s+(?:RAM|(?:LP)?DDR\w*)', hardware, re.I)
    storage = re.search(r'\b(\d+(?:\.\d+)?)\s*(GB|TB)\s+(?:PCIe\b[^.]*?\s+)?(?:NVMe\s+)?SSD', hardware, re.I)
    if not ram or int(ram[1]) < 16 or not storage:
        return None
    gb = float(storage[1]) * (1000 if storage[2].upper() == 'TB' else 1)
    if gb < 500 or not re.search(r'Windows 11', text, re.I):
        return None
    resolution = re.search(r'(\d{4})\s*[x×]\s*(\d{3,4})', text)
    full_hd = bool(resolution and int(resolution[1]) >= 1920 and int(resolution[2]) >= 1080) or bool(re.search(r'\b(?:FHD|WUXGA|2K|QHD)\b', text, re.I))
    if not full_hd:
        return None
    return {**item, 'ramGB': int(ram[1]), 'storageGB': int(gb), 'condition': 'New',
            'currency': 'CAD', 'checks': ['New from manufacturer', 'Recent Intel Core 5 / i5 or Ryzen 5 class or higher',
                                        '16 GB RAM or more', '500 GB SSD or more', 'Full HD screen or better', 'Windows 11', 'Listed in stock']}


def dell_products(source):
    rows = []
    for block in re.findall(r'<article\b[^>]*class="[^"]*ps-stack[^"]*"[^>]*>.*?</article>', source, re.S):
        p = Text(); p.feed(block)
        attrs = next((a for tag, a in p.attrs if tag == 'article'), {})
        try:
            details = json.loads(attrs['data-product-detail'])
            # Multi-configuration stacks and prices starting at are not exact offers.
            if len(details) != 1:
                continue
            d = details[0]['Value']
            specs = [plain(s) for s in re.findall(r'class="spec-label"[^>]*>(.*?)</span>', block, re.S)]
            row = qualify(dict(store='Dell Canada', title=d['title'].strip(), url=d['pdUrl'],
                               sku=d['productId'], priceCents=cents(d['dellPrice']), specs=specs,
                               inStock=attrs.get('data-is-sold-out') == 'False' and 'Starting at' not in plain(block)))
            if row: rows.append(row)
        except (KeyError, TypeError, ValueError):
            continue
    return rows


def hp_products(source):
    rows = []
    markers = list(re.finditer(r'<div\b[^>]*data-test-hook="@hpstellar/plp/product-(\d+)"[^>]*>', source))
    for n, marker in enumerate(markers):
        block = source[marker.start():markers[n+1].start() if n+1 < len(markers) else source.find('</main>', marker.end())]
        number = marker[1]
        p = Text(); p.feed(block)
        attrs = [a for tag, a in p.attrs]
        spec = next((a.get('title', '') for a in attrs if a.get('data-test-hook') == f'@hpstellar/plp/product-{number}__specs'), '')
        link = next((a for a in attrs if a.get('aria-label', '').startswith('View details ') and a.get('href')), {})
        price = re.search(r'data-test-hook="@hpstellar/plp/product-' + number + r'__price-block__sale-price"[^>]*>(.*?)</div>', block, re.S)
        stock = re.search(r'data-test-hook="@hpstellar/plp/product-' + number + r'__stock__stock"[^>]*>(.*?)</span>', block, re.S)
        sku = re.search(r'data-test-hook="@hpstellar/plp/product-' + number + r'__sku"[^>]*>(.*?)</div>', block, re.S)
        if not link or not price or not sku:
            continue
        row = qualify(dict(store='HP Canada', title=link['aria-label'][13:], url='https://www.hp.com' + link['href'],
                           sku=plain(sku[1]), priceCents=cents(plain(price[1])), specs=[s.strip() for s in spec.split(',')],
                           inStock=bool(stock and plain(stock[1]).lower() == 'in stock')))
        if row: rows.append(row)
    return rows


def compare(fetcher=fetch):
    def read(source):
        name, url = source
        try:
            rows = (dell_products if name == 'Dell Canada' else hp_products)(fetcher(url))
            return rows, dict(store=name, url=url, status='checked' if rows else 'no-verified-matches', matches=len(rows))
        except Exception:
            return [], dict(store=name, url=url, status='unavailable', matches=0)
    with ThreadPoolExecutor(max_workers=2) as pool:
        found = list(pool.map(read, SOURCES))
    unique = {r['url']:r for rows, status in found for r in rows}
    return dict(checkedAt=datetime.now(timezone.utc).isoformat(timespec='seconds'), currency='CAD',
                offers=sorted(unique.values(), key=lambda r:(r['priceCents'], r['title'])), stores=[s for _, s in found],
                scope='Lowest matching advertised price among the two manufacturer pages checked. Tax, shipping and delivery availability are not included.',
                advice='Check the exact configuration, manufacturer warranty, return window and charger before buying. Prices and stock may change at checkout.')


def cached_compare():
    global _cache, _expires
    with _lock:
        if _cache is None or time.time() >= _expires:
            _cache = compare()
            _expires = time.time() + 900
        return _cache


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = json.dumps(compare(), ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + '\n', encoding='utf-8')
    else:
        print(report)
