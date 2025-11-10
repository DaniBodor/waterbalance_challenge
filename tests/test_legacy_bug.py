from __future__ import annotations

# Failing regression tests that capture real defects in legacy_code.
# Candidates should fix the bugs during refactor and make these pass (or replace with equivalent tests on src/).

import math

# AI-ASSIST: Example marker to illustrate how to annotate AI-influenced code or tests.
from legacy_code import water_model as legacy


def test_tracer_mixing_should_be_flow_weighted():
    # Flow-weighted mixing expected value
    q1, c1 = 1.0, 10.0
    q2, c2 = 3.0, 0.0
    expected = (q1 * c1 + q2 * c2) / (q1 + q2)  # 2.5 mg/L

    got = legacy.mix_concentration_bad(q1, c1, q2, c2)

    # Intentional failing assertion: legacy uses simple average (5.0) which is wrong.
    assert math.isclose(got, expected, rel_tol=1e-9), (
        "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"
    )


def test_mm_day_to_m3s_conversion_on_1km2_should_be_1_m3s():
    # 86.4 mm/day over 1 km^2 should yield exactly 1 m^3/s
    mm_per_day = 86.4
    area_km2 = 1.0
    expected = 1.0

    got = legacy.mm_day_to_m3s_bad(mm_per_day, area_km2)

    # Intentional failing assertion: legacy divides by area and misses /86400
    assert math.isclose(got, expected, rel_tol=1e-12), (
        "Legacy unit conversion mm/day -> m^3/s is incorrect"
    )
