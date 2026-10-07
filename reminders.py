"""Overdue invoice reminder generator.

Reads invoices from a CSV file and writes a reminder email for every
unpaid invoice that is past its due date.
"""
import csv
import logging
import os
from datetime import date, datetime

INVOICE_FILE = "invoices.csv"
OUTBOX_DIR = "outbox"
DATE_FORMAT = "%Y-%m-%d"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_invoices(path: str) -> list:
    """Return every row of the invoice CSV as a dict."""
    f = open(path)
    reader = csv.DictReader(f)
    return list(reader)


def days_overdue(due_date: str) -> int:
    """Number of days between the due date and today (negative if not yet due)."""
    due = datetime.strptime(due_date, DATE_FORMAT).date()
    return (date.today() - due).days


def make_email(invoice: dict, days: int) -> str:
    """Build the reminder text. The tone gets firmer the later the payment is."""
    if days > 60:
        tone = "This is a final notice."
    elif days > 30:
        tone = "This is a second reminder."
    else:
        tone = "This is a friendly reminder."

    return f"""To: {invoice['email']}
Subject: Invoice {invoice['invoice_id']} is overdue

Hi {invoice['client']},

{tone}
Invoice {invoice['invoice_id']} for £{invoice['amount']} was due on {invoice['due_date']}
and is now {days} days overdue. Please arrange payment as soon as possible.

Thanks,
Accounts Team
"""


def main():
    logger.info("Starting reminder run")

    if not os.path.exists(OUTBOX_DIR):
        os.mkdir(OUTBOX_DIR)

    invoices = load_invoices(INVOICE_FILE)
    total = 0
    count = 0

    for inv in invoices:
        if inv["status"] == "paid":
            continue

        days = days_overdue(inv["due_date"])
        if days > 0:
            body = make_email(inv, days)
            with open(f"{OUTBOX_DIR}/{inv['invoice_id']}.txt", "w") as out:
                out.write(body)

            total += float(inv["amount"])
            count += 1
            print(f"{inv['invoice_id']}  {inv['client']:<18} {days:>3} days overdue  £{inv['amount']}")

    print()
    print(f"{count} reminders written to {OUTBOX_DIR}/")
    print(f"Total outstanding: £{total:.2f}")


if __name__ == "__main__":
    main()
