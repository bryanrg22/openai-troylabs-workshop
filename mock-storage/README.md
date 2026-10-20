# Mock object storage

**DEMO / FICTIONAL** - five synthetic invoices for the OpenAI x TroyLabs LaunchDesk workshop. No real customer information, payment instructions, addresses or bank details are included. Files are committed to Git for workshop use; they have **not** been uploaded to a cloud bucket.

## Included files

- [LD-1001 invoice](invoices/INV-DEMO-LD-1001.pdf) - Avery Lee, Wireless Keyboard, $61.48, shipped.
- [LD-1002 invoice](invoices/INV-DEMO-LD-1002.pdf) - Jordan Patel, Ergonomic Mouse, $33.19, delivered.
- [LD-1004 invoice](invoices/INV-DEMO-LD-1004.pdf) - Morgan Garcia, Laptop Stand, $105.24, returned.
- [LD-1005 invoice](invoices/INV-DEMO-LD-1005.pdf) - Cameron Kim, Noise-Canceling Headphones, $98.14, processing.
- [LD-1007 invoice](invoices/INV-DEMO-LD-1007.pdf) - Casey Brown, Desk Light, $58.58, delayed.
- [JSON manifest](manifest.json) and [CSV manifest](manifest.csv) - invoice/order/customer IDs, exact item, total in integer cents, seed date/status/tracking, MIME type, local path, object key, byte size and SHA-256.
- [Metadata schema](schema.sql) and [metadata seed](seed.sql) - optional SQLite/D1 examples, separate from the starter app.

The repository's `main` is intentionally frontend-only. Its canonical local source is [data/mock-data.json](../data/mock-data.json). Customers and orders were compared with an isolated execution of `database.py` and `data/schema.sql` from [`working-mvp` at f8a12c8](https://github.com/bryanrg22/openai-troylabs-workshop/tree/f8a12c804e37e3cb8b50f94f4224d5de809c9373); all 25 customers and 50 orders matched. No backend code was copied into the starter.

Invoice IDs are new demo identifiers. The displayed date is the **order date**, not an invented invoice issue or due date. USD is a demo display convention consistent with the frontend's dollar formatting; currency is not a seeded column. The seed does not supply quantity, unit price, taxes, shipping charges, discounts, payment or refund status, so these are not fabricated. Returned orders retain their original recorded totals; the PDFs are neither credit notes nor payment requests. JSON null tracking values remain null (blank in CSV).

## Map SQL records to object keys

Keep structured records in SQL and file bytes in object storage. See the [D1 documentation](https://developers.cloudflare.com/d1/) for SQLite-compatible records and the [R2 object model](https://developers.cloudflare.com/r2/objects/) for files addressed by keys. Sites' storage workflow uses D1 for records and R2 for files.

For LD-1007, the mapping is:

```text
customers.id = 7
  -> orders.customer_id = 7, orders.id = LD-1007
  -> invoice_assets.order_id = LD-1007
     invoice_id = INV-DEMO-LD-1007
     object_key = invoices/INV-DEMO-LD-1007.pdf
  -> R2 object bytes (application/pdf)

Local file: mock-storage/invoices/INV-DEMO-LD-1007.pdf
R2 key:    invoices/INV-DEMO-LD-1007.pdf
```

`mock-storage/` is a repository directory, **not** part of the object key. Keys are case-sensitive and are not URLs. Bucket names, download routes and access URLs are deliberately not invented. The manifest is an import inventory; SQL stores the file pointer and integrity metadata, and joins orders/customers for business fields. Seed snapshots in the manifest/PDF do not update when an order changes later.

For a future Sites implementation:

1. Keep the existing `orders` and `customers` relationships. Adapt the optional `schema.sql` through the Sites app's schema/migration system; keep the separate `seed.sql` outside schema migrations. Seed the company records before invoice metadata. These files do not create a backend on `main` and are never run automatically.
2. Declare D1 and R2 bindings in `.openai/hosting.json` when implementing a hosted Site. Preserve existing binding names; Sites starter names are normally `DB` and `BUCKET`. Sites provisions its resources through its own workflow; no separate cloud signup is needed for these fixtures.
3. Upload each manifest `local_path` as bytes under its exact `object_key` with HTTP content type `application/pdf`. Verify byte size/SHA-256, then insert the corresponding metadata. These SQL scripts alone **do not upload files**. Keep downloads unavailable until both the row and object exist.
4. On the server, find the invoice by a parameterized order lookup, then read the returned key from the R2 binding. Handle an unknown invoice and a missing object separately. Return the PDF bytes with `Content-Type: application/pdf` and a safe `Content-Disposition` filename. Access checks belong before file lookup when moving beyond this fictional demo.

Example SQL lookup (bind `LD-1007` as the parameter):

```sql
SELECT a.invoice_id, a.object_key, a.content_type,
       o.id AS order_id, o.item, o.total_cents, o.status,
       c.id AS customer_id, c.name AS customer_name
FROM invoice_assets AS a
JOIN orders AS o ON o.id = a.order_id
JOIN customers AS c ON c.id = o.customer_id
WHERE o.id = ?;
```

Use one statement per D1 `prepare()` call and `batch()` for multiple statements. `seed.sql` uses a transaction for a SQL import workflow, not a multi-statement `prepare()` call. The SQL was exercised locally with SQLite; no hosted D1/R2 deployment is claimed.

## Verify or regenerate

No extra packages are needed for the starter preview or metadata checks:

```bash
python3 mock-storage/tools/verify.py
```

Optional authoring tools use ReportLab and pypdf. Install them in a separate virtual environment; they are not application dependencies:

```bash
python3 -m venv .venv-assets
.venv-assets/bin/python -m pip install reportlab pypdf
.venv-assets/bin/python mock-storage/tools/generate.py
.venv-assets/bin/python mock-storage/tools/verify.py --pdf
```

The generator reads seeded JSON, uses integer cents, and rewrites all five PDFs, both manifests and both SQL examples together. Commit regenerated assets and metadata together. Its deterministic PDF metadata allows repeat-generation checks in the same authoring environment. For visual QA, render every PDF with `pdftoppm -png -r 110 <invoice.pdf> <output-prefix>` and inspect the pages. Changing the seed requires regenerating and reviewing the invoices.

The application server and AI agent remain workshop exercises. No credentials, hosted resources or services are created by these scripts.
