from __future__ import annotations

# Failing regression tests that capture real defects in legacy_code.
# Candidates should fix the bugs during refactor and make these pass (or replace with equivalent tests on src/).
import math
from typing import TYPE_CHECKING

from src import water_model

if TYPE_CHECKING:
    from pathlib import Path


def test_tracer_mixing_should_be_flow_weighted() -> None:
    # Flow-weighted mixing expected value
    q1, c1 = 1.0, 10.0
    q2, c2 = 3.0, 0.0
    expected = (q1 * c1 + q2 * c2) / (q1 + q2)  # 2.5 mg/L

    got = water_model.mix_concentration(q1, c1, q2, c2)

    # Intentional failing assertion: legacy uses simple average (5.0) which is wrong.
    assert math.isclose(
        got, expected, rel_tol=1e-9
    ), "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"


def test_mm_day_to_m3s_conversion_on_1km2_should_be_1_m3s() -> None:
    # 86.4 mm/day over 1 km^2 should yield exactly 1 m^3/s
    mm_per_day = 86.4
    area_km2 = 1.0
    expected = 1.0

    got = water_model.convert_mm_day_to_m3_s(mm_per_day, area_km2)

    # Intentional failing assertion: legacy divides by area and misses /86400
    assert math.isclose(
        got, expected, rel_tol=1e-12
    ), "Legacy unit conversion mm/day -> m^3/s is incorrect"


def test_write_output_csv_creates_file(tmp_path: Path) -> None:
    # Test that write_output_csv creates a file with expected content
    output_path = tmp_path / "output.csv"
    rows = [
        {"date": "2020-01-01", "reach": "A", "q_m3s": "1.0", "c_mgL": "10.0"},
        {"date": "2020-01-01", "reach": "B", "q_m3s": "2.0", "c_mgL": "5.0"},
    ]

    water_model.write_output_csv(rows, str(output_path))

    assert output_path.exists(), "Output CSV file was not created"

    with output_path.open("r", encoding="utf-8") as f:
        content = f.read()
        assert "date,reach,q_m3s,c_mgL" in content, "CSV header is missing"
        assert "2020-01-01,A,1.0,10.0" in content, "First row is missing"
        assert "2020-01-01,B,2.0,5.0" in content, "Second row is missing"


def test_model_integration() -> None:
    # Simple integration test to ensure model runs end-to-end without error
    water_model.run_all(
        forcing_path="data/forcing.csv",
        reaches_path="data/reaches.csv",
    )
