"""Local relational database populated with synthetic LaunchDesk data."""
from pathlib import Path
import sqlite3, random
from contextlib import contextmanager

ROOT = Path(__file__).parent
DB = ROOT / "launchdesk.db"
FIRST = ["Avery","Jordan","Taylor","Morgan","Cameron","Riley","Casey","Alex","Sam","Jamie","Drew","Elliot","Skyler","Quinn","Parker","Rowan","Micah","Harper","Ari","Dakota","Reese","Noah","Kai","Blair","Logan"]
LAST = ["Lee","Patel","Nguyen","Garcia","Kim","Johnson","Brown","Ramirez","Chen","Wilson"]
PRODUCTS = ["Wireless Keyboard","Ergonomic Mouse","USB-C Dock","Laptop Stand","Noise-Canceling Headphones","Webcam","Desk Light","Travel Charger"]
STATUSES = ["processing","shipped","delivered","delayed","returned"]

@contextmanager
def connection():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    finally:
        con.close()

def initialize():
    with connection() as con:
        con.executescript((ROOT / "data/schema.sql").read_text())
        if con.execute("SELECT COUNT(*) FROM customers").fetchone()[0]:
            return
        rand = random.Random(42)
        for i, name in enumerate(FIRST,1):
            lastname = LAST[(i-1) % len(LAST)]
            con.execute("INSERT INTO customers(id,name,email) VALUES(?,?,?)",(i,f"{name} {lastname}",f"customer{i:02d}@example.com"))
        for i in range(1,51):
            status = STATUSES[(i + i//7) % len(STATUSES)]
            con.execute("INSERT INTO orders VALUES(?,?,?,?,?,?,?)",(f"LD-{1000+i}", (i-1)%25+1, PRODUCTS[(i-1)%len(PRODUCTS)], status, rand.randint(2500,19000), f"TRK-DEMO-{i:05d}" if status in ("shipped","delivered","delayed") else None, f"2026-10-{(i%18)+1:02d}"))
        for i in range(1,9):
            order_id=f"LD-{1000+i*4}"
            con.execute("INSERT INTO tickets(order_id,subject,description,status) VALUES(?,?,?,?)",(order_id,["Delivery question","Return request","Tracking update","Product issue"][i%4],"Fictional starter ticket created for workshop demo.", "open" if i%3 else "resolved"))

def records(query,params=()):
    initialize()
    with connection() as con:
        return [dict(row) for row in con.execute(query,params).fetchall()]

def customers():
    return records("SELECT id,name,email FROM customers ORDER BY id")

def orders():
    return records("SELECT o.*, c.name AS customer_name FROM orders o JOIN customers c ON c.id=o.customer_id ORDER BY o.id")

def lookup_order(order_id):
    rows=records("SELECT o.*, c.name AS customer_name FROM orders o JOIN customers c ON c.id=o.customer_id WHERE o.id=?",(order_id,))
    return rows[0] if rows else None

def tickets():
    return records("SELECT * FROM tickets ORDER BY id DESC")

def summary():
    return {"customers":len(customers()),"orders":len(orders()),"tickets":len(tickets()),"open_tickets":sum(t["status"]=="open" for t in tickets())}

def create_ticket(order_id,subject,description):
    initialize()
    with connection() as con:
        cur=con.execute("INSERT INTO tickets(order_id,subject,description) VALUES(?,?,?)",(order_id,subject,description))
        row=con.execute("SELECT * FROM tickets WHERE id=?",(cur.lastrowid,)).fetchone()
        return dict(row)
