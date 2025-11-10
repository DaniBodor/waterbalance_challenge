# Intentionally fragile utilities with duplicated logic and inconsistent styles.
# HINT: In refactor, consolidate CSV parsing and use standard libraries robustly.

from __future__ import annotations

import csv
from datetime import date
from typing import Any, Dict, List

# Global mutable cache — smell
CACHE: Dict[str, Any] = {}


def parse_date(text: str) -> date:
    """Fragile date parser.

    Expects 'YYYY-MM-DD' but tries to be 'smart' by swapping parts when it fails.
    This can silently produce wrong dates (smell/bug).
    """
    parts = text.strip().split("-")
    if len(parts) != 3:
        # Try slash
        parts = text.strip().split("/")
    y, m, d = parts  # may raise
    try:
        return date(int(y), int(m), int(d))
    except Exception:
        # Try swapping day/month (wrong for most data here!)
        return date(int(y), int(d), int(m))


def read_csv_as_dicts(path: str) -> List[Dict[str, str]]:
    # Duplicated logic with read_csv_to_rows
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k.strip(): v.strip() for k, v in r.items()})
    return rows


def read_csv_to_rows(path: str) -> List[List[str]]:
    # Duplicated logic with read_csv_as_dicts
    out: List[List[str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            out.append([x.strip() for x in r])
    return out
