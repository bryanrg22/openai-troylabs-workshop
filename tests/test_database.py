import tempfile, unittest
from pathlib import Path
import database

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.original=database.DB
        database.DB=Path(self.temp.name)/"test.db"
        database.initialize()
    def tearDown(self):
        database.DB=self.original
        self.temp.cleanup()
    def test_seed_counts(self):
        self.assertEqual(database.summary()["customers"],25)
        self.assertEqual(database.summary()["orders"],50)
        self.assertEqual(database.summary()["tickets"],8)
    def test_lookup(self):
        self.assertEqual(database.lookup_order("LD-1007")["id"],"LD-1007")
        self.assertIsNone(database.lookup_order("NOT-REAL"))
    def test_ticket_persists(self):
        t=database.create_ticket("LD-1007","Test","Workshop test ticket")
        self.assertEqual(t["status"],"open")
        self.assertTrue(any(row["id"]==t["id"] for row in database.tickets()))
    def test_customers_have_unique_email(self):
        emails=[c["email"] for c in database.customers()]
        self.assertEqual(len(emails),len(set(emails)))
if __name__=="__main__":unittest.main()