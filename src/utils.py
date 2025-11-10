# Intentionally fragile utilities with duplicated logic and inconsistent styles.
# HINT: In refactor, consolidate CSV parsing and use standard libraries robustly.

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


def parse_date(text: str) -> str:
    """Date parser.

    Expects 'YYYY-MM-DD' or 'YYYY/MM/DD' which is converted back to 'YYYY-MM-DD'.
    """
    parts = text.strip().split("-")
    if len(parts) != 3:
        # Try slash
        parts = text.strip().split("/")
    y, m, d = parts  # may raise
    try:
        return date(int(y), int(m), int(d)).isoformat()
    except ValueError as e:
        msg = f"Date not recognized. Expected date format: YYYY-MM-DD (e.g. 2020-12-31). Got: {text}."
        raise ValueError(msg) from e


def read_csv_as_dicts(path: str) -> list[dict[str, str]]:
    # Duplicated logic with read_csv_to_rows
    rows: list[dict[str, str]] = []
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k.strip(): v.strip() for k, v in r.items()})
    return rows


def read_csv_to_rows(path: str) -> list[list[str]]:
    # Duplicated logic with read_csv_as_dicts
    out: list[list[str]] = []
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            out.append([x.strip() for x in r])
    return out
