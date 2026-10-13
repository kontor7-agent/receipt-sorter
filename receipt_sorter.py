#!/usr/bin/env python3
"""receipt-sorter: sort a folder of receipt files into YEAR/YYYY-MM subfolders.

- Dry-run by default: prints what WOULD happen. Add --apply to move files.
- Only touches files inside the folder you point it at. Never deletes anything.
- Never overwrites: name clashes get a _2, _3 ... suffix.
- No network access, no dependencies (Python 3.8+ standard library only).
- Writes receipt-index.csv (old path, new path, date, source of date) when applying.
"""
import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".heic", ".gif", ".webp", ".tif",
        ".tiff", ".xml", ".eml", ".csv", ".txt", ".docx", ".xlsx"}
OUT_NAME = "sorted"
DATE_RE = re.compile(r"(?<!\d)(20\d{2})[-_.]?(0[1-9]|1[0-2])[-_.]?(0[1-9]|[12]\d|3[01])(?!\d)")


def find_date(path):
    m = DATE_RE.search(path.name)
    if m:
        try:
            return dt.date(int(m[1]), int(m[2]), int(m[3])), "filename"
        except ValueError:
            pass
    return dt.date.fromtimestamp(path.stat().st_mtime), "modified-time"


def unique(dest):
    if not dest.exists():
        return dest
    n = 2
    while True:
        cand = dest.with_name(f"{dest.stem}_{n}{dest.suffix}")
        if not cand.exists():
            return cand
        n += 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sort receipt files into YEAR/YYYY-MM folders (dry-run by default).")
    ap.add_argument("folder", help="folder containing receipt files")
    ap.add_argument("--apply", action="store_true", help="really move the files (default: preview only)")
    ap.add_argument("--year", type=int, help="only handle receipts of this year")
    ap.add_argument("--recursive", action="store_true", help="also look in subfolders (the output folder is skipped)")
    args = ap.parse_args(argv)

    root = Path(args.folder).resolve()
    if not root.is_dir():
        print(f"Not a folder: {root}", file=sys.stderr)
        return 2
    out = root / OUT_NAME

    it = root.rglob("*") if args.recursive else root.glob("*")
    files = sorted(p for p in it if p.is_file() and not p.is_symlink()
                   and p.suffix.lower() in EXTS and out not in p.parents
                   and p.name != "receipt-index.csv")
    rows, counts = [], {}
    for p in files:
        d, src = find_date(p)
        if args.year and d.year != args.year:
            continue
        dest_dir = out / str(d.year) / f"{d.year}-{d.month:02d}"
        dest = unique(dest_dir / p.name)
        # safety: destination must stay inside the target folder
        if root not in dest.resolve().parents:
            continue
        rows.append((p, dest, d, src))
        counts[d.year] = counts.get(d.year, 0) + 1
        print(f"{'MOVE' if args.apply else 'would move'}: {p.relative_to(root)} -> {dest.relative_to(root)}  [{src}]")
        if args.apply:
            dest.parent.mkdir(parents=True, exist_ok=True)
            p.rename(dest)

    if not rows:
        print("No matching receipt files found.")
        return 0
    if args.apply:
        idx = out / "receipt-index.csv"
        new = not idx.exists()
        with idx.open("a", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(["old_path", "new_path", "date", "date_source"])
            for p, dest, d, src in rows:
                w.writerow([str(p), str(dest), d.isoformat(), src])
        print(f"\nMoved {len(rows)} file(s). Index: {idx}")
    else:
        print(f"\nDry run: {len(rows)} file(s) would be moved. Re-run with --apply to do it.")
    for y in sorted(counts):
        print(f"  {y}: {counts[y]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
