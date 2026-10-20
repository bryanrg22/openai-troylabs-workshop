-- DEMO / FICTIONAL. Optional metadata schema, never applied at app startup.
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
