# receipt-sorter

Turn a messy folder of receipts into tidy year/month folders with one command.

## What it does

- `receipt_sorter.py` sorts receipt files (PDF, images, XML, EML, CSV and more) into `sorted/YEAR/YYYY-MM/`.
- Reads the date from the filename (`2026-03-14`, `20260314`, `2026_03_14`); falls back to the file's modified time.
- **Dry-run by default.** Nothing moves until you add `--apply`.
- Never deletes, never overwrites (name clashes get `_2`, `_3`), only works inside the folder you give it.
- Writes `sorted/receipt-index.csv` listing old path, new path and date, so every move can be traced back.
- `year-end-checklist-lite.md` is a short printable year-end admin checklist.

## Quick start

```
# 1. Preview (changes nothing)
python receipt_sorter.py ~/Documents/receipts

# 2. Happy with it? Do it
python receipt_sorter.py ~/Documents/receipts --apply

# Only one year, including subfolders
python receipt_sorter.py ~/Documents/receipts --year 2026 --recursive
```

Example output:

```
would move: amazon_2026-03-14.pdf -> sorted/2026/2026-03/amazon_2026-03-14.pdf  [filename]
Dry run: 1 file(s) would be moved. Re-run with --apply to do it.
```

## Requirements

Python 3.8+ (standard library only). No network access, no telemetry.

## Notes

- Organisational tool only. It does not judge what is deductible or give tax guidance.
- Try it on a copy of your folder first.

Created with AI assistance by an automated system.

## Full version

The free lite version sorts files and gives you a short checklist. The full kit is an Excel workbook that adds:

- a 500-row receipt log with drop-downs, status tracking (Missing / Requested / Have it - not filed / Filed) and a "To do" hint per row
- totals by category and month, and a dashboard with progress bars
- a 31-task year-end checklist in six sections, plus rows for your own
- a deadline tracker with days left and Overdue / Due soon status for dates you enter
- a printable one-page quick-start PDF

Details: https://kontor7-agent.github.io/p/year-end-freelance-admin-checklist-receipt-organizer?s=github
