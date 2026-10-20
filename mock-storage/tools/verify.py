"""Validate fixture integrity, seed parity, and optional PDF text; no cloud calls."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
STORAGE = ROOT / 'mock-storage'
EXPECTED = {'LD-1001', 'LD-1002', 'LD-1004', 'LD-1005', 'LD-1007'}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', action='store_true', help='also inspect PDF text using pypdf')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/mock-data.json').read_text())
    orders = {o['id']: o for o in data['orders']}
    customers = {c['id']: c for c in data['customers']}
    rows = json.loads((STORAGE / 'manifest.json').read_text())
    check(len(rows) == 5 and {r['order_id'] for r in rows} == EXPECTED, 'Wrong invoice coverage')
    with (STORAGE / 'manifest.csv').open(newline='') as f:
        check(list(csv.DictReader(f)) == [{k: '' if v is None else str(v) for k, v in r.items()} for r in rows], 'CSV/JSON mismatch')
    check({p.relative_to(STORAGE).as_posix() for p in (STORAGE / 'invoices').glob('*')} == {r['object_key'] for r in rows}, 'Missing or extra invoices')
    for row in rows:
        o = orders[row['order_id']]; c = customers[o['customer_id']]
        for manifest_key, seed_key in [('customer_id', 'customer_id'), ('item', 'item'), ('total_cents', 'total_cents'), ('tracking', 'tracking'), ('order_status', 'status'), ('order_created_at', 'created_at')]:
            check(row[manifest_key] == o[seed_key], f"Seed mismatch: {manifest_key}")
        check(row['customer_name'] == c['name'] and row['customer_email'] == c['email'], 'Customer mismatch')
        check(row['customer_email'].endswith('@example.com'), 'Non-demo email')
        check(row['invoice_id'] == f"INV-DEMO-{o['id']}", 'Invoice ID mismatch')
        check(row['object_key'] == f"invoices/{row['invoice_id']}.pdf", 'Unexpected object key')
        check(row['local_path'] == f"mock-storage/{row['object_key']}", 'Local path mismatch')
        check(row['content_type'] == 'application/pdf' and row['demo_label'] == 'DEMO / FICTIONAL', 'Missing demo/MIME metadata')
        check(row['currency'] == 'USD', 'Unexpected display currency')
        content = (ROOT / row['local_path']).read_bytes()
        check(content.startswith(b'%PDF-'), 'Not a PDF')
        check(len(content) == row['size_bytes'] and hashlib.sha256(content).hexdigest() == row['sha256'], 'File integrity mismatch')
        if args.pdf:
            from pypdf import PdfReader
            pdf = PdfReader(ROOT / row['local_path'])
            check(len(pdf.pages) == 1, 'Expected one-page invoice')
            text = pdf.pages[0].extract_text()
            for value in [row['invoice_id'], row['order_id'], c['name'], c['email'], o['item'], o['status'], o['created_at'], o['tracking'] or 'Not recorded in seed', f"${o['total_cents']//100:,}.{o['total_cents']%100:02d}"]:
                check(str(value) in text, f'PDF missing expected content: {value}')
            check(text.count('DEMO / FICTIONAL') == 2, 'Missing visible demo labels')
            check('not a payment request' in text and 'synthetic' in text, 'Missing fictional-use notice')
    # Verify actual joins, repeated seed, constraints, nulls and unknown-order behavior.
    with sqlite3.connect(':memory:') as db:
        db.execute('PRAGMA foreign_keys=ON')
        db.executescript('CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, email TEXT); CREATE TABLE orders(id TEXT PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), item TEXT, status TEXT, total_cents INTEGER, tracking TEXT, created_at TEXT);')
        db.executemany('INSERT INTO customers VALUES (:id,:name,:email)', data['customers'])
        db.executemany('INSERT INTO orders VALUES (:id,:customer_id,:item,:status,:total_cents,:tracking,:created_at)', data['orders'])
        db.commit()
        db.executescript((STORAGE / 'schema.sql').read_text())
        for _ in range(2):
            db.executescript((STORAGE / 'seed.sql').read_text())
        check(db.execute('SELECT COUNT(*) FROM invoice_assets').fetchone()[0] == 5, 'Repeated seed duplicates rows')
        for r in rows:
            result = db.execute('SELECT a.invoice_id,a.object_key,a.content_type,o.total_cents,c.name,o.tracking,a.size_bytes,a.sha256 FROM invoice_assets a JOIN orders o ON o.id=a.order_id JOIN customers c ON c.id=o.customer_id WHERE o.id=?', (r['order_id'],)).fetchone()
            check(result == tuple(r[k] for k in ['invoice_id','object_key','content_type','total_cents','customer_name','tracking','size_bytes','sha256']), 'SQL mapping mismatch')
        check(db.execute('SELECT * FROM invoice_assets WHERE order_id=?', ('LD-MISSING',)).fetchone() is None, 'Missing order lookup')
        check(db.execute('SELECT * FROM invoice_assets WHERE order_id=?', ('LD-1003',)).fetchone() is None, 'Unattached order lookup')
        invalid_updates = ["order_id='LD-MISSING'", "order_id='LD-1001'", "object_key='invoices/INV-DEMO-LD-1001.pdf'", "content_type='text/html'", "size_bytes=0", "sha256='bad'", "demo_label='real'"]
        for update in invalid_updates:
            try:
                db.execute(f"UPDATE invoice_assets SET {update} WHERE order_id='LD-1007'")
            except sqlite3.IntegrityError:
                db.rollback()
            else:
                raise ValueError(f'Constraint failed to reject: {update}')
        check(db.execute('SELECT COUNT(*) FROM orders').fetchone()[0] == 50, 'Orders changed')
        check(db.execute('SELECT COUNT(*) FROM customers').fetchone()[0] == 25, 'Customers changed')
    print('PASS: five invoices; seed parity; manifest integrity; SQL joins, idempotency and constraints' + ('; PDF content and labels' if args.pdf else ' (PDF text check not requested)'))


if __name__ == '__main__':
    main()
