"""LaunchDesk workshop MVP: run with python3 server.py, then open http://localhost:8000."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, sqlite3, mimetypes
import database

ROOT = Path(__file__).parent
STATIC = ROOT / "public"

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path)
        try:
            if path.path == "/api/summary":
                return self.respond(200, database.summary())
            if path.path == "/api/orders":
                return self.respond(200, database.orders())
            if path.path == "/api/customers":
                return self.respond(200, database.customers())
            if path.path == "/api/tickets":
                return self.respond(200, database.tickets())
            if path.path == "/api/policies":
                return self.respond(200, {"text": (ROOT / "data/company-policies.md").read_text()})
            if path.path.startswith("/api/orders/"):
                result = database.lookup_order(path.path.split("/")[-1])
                return self.respond(200 if result else 404, result or {"error":"Order not found"})
            if path.path.startswith("/api/"):
                return self.respond(404, {"error":"API endpoint not found"})
            target = (STATIC / path.path.lstrip("/")).resolve() if path.path != "/" else STATIC / "index.html"
            if not target.is_relative_to(STATIC.resolve()) or not target.is_file():
                return self.respond(404, {"error":"Not found"})
            body = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:
            print("GET error:", exc)
            self.respond(500, {"error":"Internal server error"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 8192:
                return self.respond(413, {"error":"Request body must be 1–8192 bytes"})
            payload = json.loads(self.rfile.read(length))
            if self.path == "/api/tickets":
                order_id = str(payload.get("order_id","")).strip()
                subject = str(payload.get("subject","")).strip()
                description = str(payload.get("description","")).strip()
                if not order_id or not (1 <= len(subject) <= 120) or not (1 <= len(description) <= 2000):
                    return self.respond(400, {"error":"Provide an order, subject (1–120), and description (1–2000)"})
                if not database.lookup_order(order_id):
                    return self.respond(404, {"error":"Order not found"})
                return self.respond(201, database.create_ticket(order_id,subject,description))
            if self.path == "/api/chat":
                return self.respond(501, {"error":"AI support agent not connected yet. Use Codex workshop exercise 2 to implement it!"})
            return self.respond(404, {"error":"API endpoint not found"})
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self.respond(400, {"error":"Expected valid JSON"})
        except Exception as exc:
            print("POST error:", exc)
            return self.respond(500, {"error":"Internal server error"})

if __name__ == "__main__":
    database.initialize()
    print("LaunchDesk is running at http://localhost:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
