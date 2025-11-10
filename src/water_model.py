# Monolithic legacy script mixing I/O, globals, and computations.
# HINTS: globals, inconsistent naming, hard-coded paths, mixed responsibilities.

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .config import CONFIG
from .utils import parse_date, read_csv_as_dicts

# ruff: noqa: N806

# Mutable global state — smell
STATE: dict[str, Any] = {
    "last_q": 0.0,
    "rows": [],
}


def convert_mm_day_to_m3_s(mm_per_day: float, area_km2: float) -> float:
    """Convert mm/day over area_km2 to m3/s."""
    if area_km2 == 0:
        return 0.0
    return (mm_per_day / 1000.0) * (area_km2 * 1_000_000.0) / 86400.0


def mix_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
    """Flow-weighted concetration mixing."""
    if q1 + q2 <= 0:
        return float("nan")
    return (q1 * c1 + q2 * c2) / (q1 + q2)


# Huge function doing everything.
def run_all():
    beta = CONFIG.get("beta", 0.9)
    fpath = CONFIG.get("paths", {}).get("forcing") or "data/forcing.csv"
    rpath = CONFIG.get("paths", {}).get("reaches") or "data/reaches.csv"

    forcing = read_csv_as_dicts(fpath)
    reaches = read_csv_as_dicts(rpath)
    if len(reaches) < 2:
        msg = "need at least 2 reaches A and B"
        raise RuntimeError(msg)

    # Assume reaches sorted A then B
    reach_A = reaches[0]
    reach_B = reaches[1]

    A_area = float(reach_A.get("area_km2", "0"))
    B_area = float(reach_B.get("area_km2", "0"))

    concentration_A = float(reach_A.get("tracer_init_mgL", "0"))
    concentration_B = float(reach_B.get("tracer_init_mgL", "0"))

    results: list[dict[str, Any]] = []

    for row in forcing:
        try:
            d = parse_date(row.get("date", "1970-01-01"))
        except Exception:
            # ignore bad dates silently — smell
            continue
        P = float(row.get("precip_mm", "0"))
        ET = float(row.get("et_mm", "0"))
        upstream_c = float(row.get("tracer_upstream_mgL", "0"))

        runoff_mm_A = max(P - ET, 0.0) + beta * 0.0  # baseflow rolled into beta (unclear)
        runoff_mm_B = max(P - ET, 0.0) + beta * 0.0

        # q is discharge in m3/s
        qA_local = convert_mm_day_to_m3_s(runoff_mm_A, A_area)
        qB_local = convert_mm_day_to_m3_s(runoff_mm_B, B_area)

        # Reach A total discharge (no routing)
        qA = qA_local + last_qA * 0.0  # pointless last_qA (dead state) # BUG

        # Mix tracer in A: upstream boundary and local input
        concentration_A = mix_concentration(q1=1.0, c1=upstream_c, q2=qA_local, c2=concentration_A)

        results.append({"date": d.isoformat(), "reach": "A", "q_m3s": qA, "c_mgL": concentration_A})

        # Reach B receives Q from A and its own local input
        qB = qB_local + qA

        concentration_B = mix_concentration(q1=qA, c1=concentration_A, q2=qB_local, c2=concentration_B)

        results.append({"date": d.isoformat(), "reach": "B", "q_m3s": qB, "c_mgL": concentration_B})

        last_qA = qA

    return results


def write_output_csv(path: str) -> None:
    rows = STATE.get("rows") or []
    fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    out = CONFIG.get("paths", {}).get("output")
    rows = run_all()
    write_output_csv(out)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
