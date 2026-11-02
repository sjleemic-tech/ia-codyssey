#!/usr/bin/env python3
"""
Simple attendance recorder (no external libraries)

Usage examples:
  python attend.py add --name "홍길동" --date 2026-11-02
  python attend.py add --name "김철수"        # date omitted -> today
  python attend.py list

This program stores records in attendance.csv (columns: date,name).
Date format: YYYY-MM-DD
"""
import argparse
import csv
import datetime
import os
import sys

FNAME = "attendance.csv"
HEADER = ["date", "name"]

def ensure_file():
    """If CSV doesn't exist, create it with header."""
    if not os.path.exists(FNAME):
        with open(FNAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

def validate_date(date_str):
    """Validate YYYY-MM-DD. Raise ValueError if invalid."""
    try:
        return datetime.date.fromisoformat(date_str).isoformat()
    except Exception:
        raise ValueError("날짜 형식은 YYYY-MM-DD 이어야 합니다. 예: 2026-11-02")

def add_entry(name, date_str=None):
    """Append one attendance record to CSV."""
    if not name:
        raise ValueError("이름은 비워둘 수 없습니다.")
    if date_str:
        date_iso = validate_date(date_str)
    else:
        date_iso = datetime.date.today().isoformat()
    ensure_file()
    with open(FNAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_iso, name])
    print(f"Added: {date_iso}  -  {name}")

def read_entries():
    """Return list of dicts from CSV (empty list if no file)."""
    if not os.path.exists(FNAME):
        return []
    with open(FNAME, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def list_entries():
    """Print all records (sorted by date then name)."""
    entries = read_entries()
    if not entries:
        print("No records.")
        return
    # try to sort by date then name for nicer display
    try:
        entries.sort(key=lambda e: (e["date"], e["name"]))
    except KeyError:
        pass
    print("date\t\tname")
    print("-" * 30)
    for e in entries:
        print(f"{e.get('date','')}\t{e.get('name','')}")

def parse_args(argv):
    p = argparse.ArgumentParser(description="Attendance CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="Add attendance record")
    a.add_argument("--name", "-n", required=True, help="Name (e.g. '홍길동')")
    a.add_argument("--date", "-d", required=False, help="Date YYYY-MM-DD (omit for today)")

    sub.add_parser("list", help="List all attendance records")

    return p.parse_args(argv)

def main(argv):
    args = parse_args(argv)
    try:
        if args.cmd == "add":
            add_entry(args.name.strip(), args.date)
        elif args.cmd == "list":
            list_entries()
    except ValueError as e:
        print("Error:", e)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
