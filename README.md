# Invoice Reminder Automation

A small demo script that reads `invoices.csv`, finds unpaid invoices past their due date, and writes a reminder email (as a text file) for each into `outbox/`.

Reminder tone escalates with age: friendly (up to 30 days), second reminder (31–60), final notice (60+).

## Run

    python3 reminders.py

No dependencies. Python 3.8+.
