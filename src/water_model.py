# Monolithic legacy script mixing I/O, globals, and computations.
# HINTS: globals, inconsistent naming, hard-coded paths, mixed responsibilities.

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any

from .config import FORCING_PATH, MM_DAY_TO_M3_S, OUTPUT_PATH, REACHES_PATH
from .utils import parse_date, read_csv_as_dicts

# AI-ASSIST: Remove the (mutable) global CONFIG from codebase.

logger = logging.getLogger(__name__)


def convert_mm_day_to_m3_s(mm_per_day: float, area_km2: float) -> float:
    """Convert mm/day over area_km2 to m3/s."""
    if area_km2 == 0:
        return 0.0
    return mm_per_day * area_km2 * MM_DAY_TO_M3_S


def mix_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
    """Flow-weighted concetration mixing."""
    if q1 + q2 <= 0:
        return float("nan")
    return (q1 * c1 + q2 * c2) / (q1 + q2)


# AI-ASSIST: refactor `run_all` into modular structure
class ReachData:
    """Data container for a single reach."""

    def __init__(self, reach_dict: dict[str, str], reach_id: str):
        self.id = reach_id
        self.area_km2 = float(reach_dict.get("area_km2", "0"))
        self.tracer_concentration = float(reach_dict.get("tracer_init_mgL", "0"))


def load_input_data(forcing_path: str, reaches_path: str) -> tuple[list[dict[str, str]], list[ReachData]]:
    """Load forcing and reach data from CSV files.

    Args:
        forcing_path: Path to forcing data CSV
        reaches_path: Path to reaches data CSV

    Returns:
        Tuple of (forcing data, reach data objects)

    Raises:
        RuntimeError: If fewer than 2 reaches are found
    """
    forcing = read_csv_as_dicts(forcing_path)
    reaches_raw = read_csv_as_dicts(reaches_path)

    if len(reaches_raw) < 2:
        msg = "need at least 2 reaches A and B"
        raise RuntimeError(msg)

    # Create ReachData objects for first two reaches (A and B)
    reaches = [
        ReachData(reaches_raw[0], "A"),
        ReachData(reaches_raw[1], "B"),
    ]

    return forcing, reaches


def calculate_runoff(precip_mm: float, et_mm: float) -> float:
    """Calculate runoff in mm/day.

    Args:
        precip_mm: Precipitation in mm/day
        et_mm: Evapotranspiration in mm/day

    Returns:
        Runoff in mm/day
    """
    # baseflow (beta) is not taken into account here.
    return max(precip_mm - et_mm, 0.0)


def process_reach_a(
    date: str,
    runoff_mm: float,
    reach: ReachData,
    upstream_concentration: float,
) -> dict[str, Any]:
    """Process a single timestep for reach A.

    Args:
        date: Date string for this timestep
        runoff_mm: Runoff in mm/day
        reach: ReachData object for reach A
        upstream_concentration: Upstream boundary tracer concentration

    Returns:
        Result dictionary with date, reach, discharge, and concentration
    """
    q_local = convert_mm_day_to_m3_s(runoff_mm, reach.area_km2)

    # Mix tracer: upstream boundary and local input
    reach.tracer_concentration = mix_concentration(
        q1=1.0,
        c1=upstream_concentration,
        q2=q_local,
        c2=reach.tracer_concentration,
    )

    return {
        "date": date,
        "reach": reach.id,
        "q_m3s": q_local,
        "c_mgL": reach.tracer_concentration,
    }


def process_reach_b(
    date: str,
    runoff_mm: float,
    reach_b: ReachData,
    upstream_q: float,
    upstream_concentration: float,
) -> dict[str, Any]:
    """Process a single timestep for reach B.

    Args:
        date: Date string for this timestep
        runoff_mm: Runoff in mm/day
        reach_b: ReachData object for reach B
        upstream_q: Discharge from upstream reach A in m3/s
        upstream_concentration: Tracer concentration from upstream reach A

    Returns:
        Result dictionary with date, reach, discharge, and concentration
    """
    q_local = convert_mm_day_to_m3_s(runoff_mm, reach_b.area_km2)
    q_total = q_local + upstream_q

    # Mix tracer: upstream from A and local input
    reach_b.tracer_concentration = mix_concentration(
        q1=upstream_q,
        c1=upstream_concentration,
        q2=q_local,
        c2=reach_b.tracer_concentration,
    )

    return {
        "date": date,
        "reach": reach_b.id,
        "q_m3s": q_total,
        "c_mgL": reach_b.tracer_concentration,
    }


def simulate_timestep(
    forcing_row: dict[str, str],
    reach_a: ReachData,
    reach_b: ReachData,
) -> list[dict[str, Any]]:
    """Simulate a single timestep for all reaches.

    Args:
        forcing_row: Dictionary with forcing data for this timestep
        reach_a: ReachData object for reach A
        reach_b: ReachData object for reach B

    Returns:
        List of result dictionaries (one per reach)
    """
    date = parse_date(forcing_row.get("date", "1970-01-01"))
    precip_mm = float(forcing_row.get("precip_mm", "0"))
    et_mm = float(forcing_row.get("et_mm", "0"))
    upstream_c = float(forcing_row.get("tracer_upstream_mgL", "0"))

    runoff_mm = calculate_runoff(precip_mm, et_mm)

    # Process reach A
    result_a = process_reach_a(date, runoff_mm, reach_a, upstream_c)

    # Process reach B (receives output from A)
    result_b = process_reach_b(
        date,
        runoff_mm,
        reach_b,
        upstream_q=result_a["q_m3s"],
        upstream_concentration=result_a["c_mgL"],
    )

    return [result_a, result_b]


def run_simulation(
    forcing: list[dict[str, str]],
    reaches: list[ReachData],
) -> list[dict[str, Any]]:
    """Run the water balance simulation for all timesteps.

    Args:
        forcing: List of forcing data dictionaries
        reaches: List of ReachData objects

    Returns:
        List of result dictionaries for all reaches and timesteps
    """
    reach_a, reach_b = reaches[0], reaches[1]
    all_results: list[dict[str, Any]] = []

    for row in forcing:
        timestep_results = simulate_timestep(row, reach_a, reach_b)
        all_results.extend(timestep_results)

    return all_results


def run_all(forcing_path: str = FORCING_PATH, reaches_path: str = REACHES_PATH) -> list[dict[str, Any]]:
    """Main entry point for running the water balance model.

    Loads configuration, reads input data, runs simulation, and returns results.
    """
    forcing, reaches = load_input_data(forcing_path, reaches_path)
    return run_simulation(forcing, reaches)


def write_output_csv(rows: list[dict[str, Any]], output_path: str = OUTPUT_PATH) -> None:
    """Write results to CSV file.

    Args:
        rows: List of result dictionaries to write
        output_path: Output file path
    """
    fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
    with Path(output_path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    out = OUTPUT_PATH
    rows = run_all()
    write_output_csv(rows, out)
    logger.info("Wrote %d rows to %s", len(rows), out)


if __name__ == "__main__":
    main()
