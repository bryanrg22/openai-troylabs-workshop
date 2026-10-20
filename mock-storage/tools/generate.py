"""Regenerate DEMO / FICTIONAL invoices and metadata from the starter seed.

Optional authoring dependency: reportlab. The application does not need it.
Run from any directory: python3 mock-storage/tools/generate.py
"""
import csv
import hashlib
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
STORAGE = ROOT / "mock-storage"
ORDER_IDS = ("LD-1001", "LD-1002", "LD-1004", "LD-1005", "LD-1007")
LABEL = "DEMO / FICTIONAL"


def money(cents):
    return f"${cents // 100:,}.{cents % 100:02d}"


def invoice(row, target):
    c = canvas.Canvas(str(target), pagesize=(612, 792), invariant=1)
    c.setTitle(f"{LABEL} | {row['invoice_id']} | {row['order_id']}")
    c.setAuthor("LaunchDesk fictional workshop company")
    navy, muted, teal = "#142C38", "#536974", "#087E83"

    def text(x, y, value, size=10, color=navy, bold=False):
        c.setFillColor(HexColor(color))
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, str(value))

    def right(x, y, value, size=10, color=navy, bold=False):
        c.setFillColor(HexColor(color))
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawRightString(x, y, str(value))

    c.setFillColor(HexColor(navy)); c.rect(0, 644, 612, 148, fill=1, stroke=0)
    c.setFillColor(HexColor(teal)); c.rect(0, 784, 612, 8, fill=1, stroke=0)
    text(44, 739, "LaunchDesk", 28, "#FFFFFF", True)
    text(44, 716, "Workspace essentials. Thoughtful support.", 10, "#BDCFD5")
    right(568, 740, "INVOICE", 12, "#FFFFFF", True)
    right(568, 718, row['invoice_id'], 10, "#BDCFD5")
    text(44, 674, LABEL, 11, "#A9E8E1", True)
    right(568, 674, "OpenAI x TroyLabs workshop", 9, "#BDCFD5")

    text(44, 611, "BILL TO / SYNTHETIC CUSTOMER", 8, muted, True)
    text(44, 586, row['customer_name'], 18, navy, True)
    text(44, 566, row['customer_email'], 10, muted)
    text(44, 547, f"Customer ID: {row['customer_id']}", 10, muted)
    text(370, 611, "ORDER REFERENCE", 8, muted, True)
    text(370, 586, row['order_id'], 18, navy, True)
    text(370, 566, f"Order date: {row['order_created_at']}", 10, muted)
    text(370, 547, f"Seed status: {row['order_status']}", 10, muted)

    c.setFillColor(HexColor("#EEF4F5")); c.roundRect(44, 477, 524, 36, 5, fill=1, stroke=0)
    text(58, 490, "ORDER ITEM", 9, muted, True)
    right(554, 490, "RECORDED AMOUNT", 9, muted, True)
    text(58, 449, row['item'], 12, navy, True)
    right(554, 449, money(row['total_cents']), 12, navy, True)
    c.setStrokeColor(HexColor("#D6E0E3")); c.line(44, 428, 568, 428)
    text(44, 403, "Recorded order total", 11, muted)
    right(568, 397, money(row['total_cents']), 27, teal, True)
    right(568, 379, "USD - demo presentation currency", 8, muted)
    text(44, 358, "No tax, shipping or discount breakdown is supplied by the seed.", 9, muted)
    text(44, 342, "Payment and refund state are not recorded. This is not a payment request.", 9, muted)

    c.setFillColor(HexColor("#F4F7F7")); c.roundRect(44, 206, 524, 100, 6, fill=1, stroke=0)
    text(60, 282, "FULFILLMENT SNAPSHOT", 8, muted, True)
    text(60, 258, f"Tracking: {row['tracking'] or 'Not recorded in seed'}", 11, navy, True)
    text(60, 235, "Status reflects the workshop seed; no live shipment or carrier is implied.", 9, muted)
    text(44, 169, "For learning, lookup and file-storage demonstrations only.", 10, navy, True)
    text(44, 151, "All identities and transactions are synthetic. No goods or services are owed.", 9, muted)
    c.setStrokeColor(HexColor("#D6E0E3")); c.line(44, 96, 568, 96)
    text(44, 76, LABEL, 9, teal, True)
    right(568, 76, f"{row['order_id']}  /  Page 1 of 1", 9, muted)
    c.showPage(); c.save()


def main():
    data = json.loads((ROOT / "data/mock-data.json").read_text())
    customers = {x['id']: x for x in data['customers']}
    orders = {x['id']: x for x in data['orders']}
    (STORAGE / "invoices").mkdir(parents=True, exist_ok=True)
    rows = []
    for order_id in ORDER_IDS:
        o = orders[order_id]; customer = customers[o['customer_id']]
        invoice_id = f"INV-DEMO-{order_id}"
        key = f"invoices/{invoice_id}.pdf"
        row = dict(demo_label=LABEL, invoice_id=invoice_id, order_id=order_id,
                   customer_id=customer['id'], customer_name=customer['name'],
                   customer_email=customer['email'], item=o['item'],
                   total_cents=o['total_cents'], currency="USD",
                   order_status=o['status'], order_created_at=o['created_at'],
                   tracking=o['tracking'], content_type="application/pdf", object_key=key,
                   local_path=f"mock-storage/{key}")
        target = STORAGE / key
        invoice(row, target)
        row.update(size_bytes=target.stat().st_size,
                   sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        rows.append(row)
    (STORAGE / "manifest.json").write_text(json.dumps(rows, indent=2) + "\n")
    with (STORAGE / "manifest.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); writer.writeheader(); writer.writerows(rows)

    # Separate schema and seed, so a future Sites app can manage schema migrations.
    schema = '''-- DEMO / FICTIONAL. Optional metadata schema, never applied at app startup.
-- Requires the existing orders table. Port through the Sites app's migration system.
CREATE TABLE IF NOT EXISTS invoice_assets (
    invoice_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL UNIQUE REFERENCES orders(id),
    object_key TEXT NOT NULL UNIQUE,
    content_type TEXT NOT NULL CHECK (content_type = 'application/pdf'),
    size_bytes INTEGER NOT NULL CHECK (size_bytes > 0),
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
    demo_label TEXT NOT NULL CHECK (demo_label = 'DEMO / FICTIONAL')
);
'''
    (STORAGE / "schema.sql").write_text(schema)
    def literal(value):
        return str(value) if isinstance(value, int) else "'" + value.replace("'", "''") + "'"
    fields = ('invoice_id', 'order_id', 'object_key', 'content_type', 'size_bytes', 'sha256', 'demo_label')
    statements = ["-- DEMO / FICTIONAL. Seed only after orders exist and schema.sql has been applied.", "BEGIN TRANSACTION;"]
    for row in rows:
        statements.append(f"INSERT INTO invoice_assets ({', '.join(fields)}) VALUES ({', '.join(literal(row[k]) for k in fields)}) ON CONFLICT(invoice_id) DO UPDATE SET " + ', '.join(f"{k}=excluded.{k}" for k in fields[1:]) + ';')
    statements.append("COMMIT;")
    (STORAGE / "seed.sql").write_text('\n'.join(statements) + '\n')
    print(f"Generated {len(rows)} DEMO / FICTIONAL invoices, two manifests and SQL examples.")


if __name__ == '__main__':
    main()
