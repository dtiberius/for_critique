import unittest

from reminders import days_overdue, make_email


class TestReminders(unittest.TestCase):
    def test_days_overdue(self):
        self.assertEqual(days_overdue("2026-08-15"), 53)

    def test_email_has_client_name(self):
        inv = {
            "invoice_id": "INV-1",
            "client": "Acme",
            "email": "a@acme.example",
            "amount": "100.00",
            "due_date": "2026-01-01",
        }
        email = make_email(inv, 10)
        self.assertIn("Acme", email)


if __name__ == "__main__":
    unittest.main()
