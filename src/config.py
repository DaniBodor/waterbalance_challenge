# WARNING: This is intentionally messy legacy config with magic strings.
# HINT: Avoid global mutable config and magic keys in refactor.

CONFIG = {
    "beta": 0.85,  # recession/baseflow factor (unitless)
    "conversion": {
        # Correct should be: mm/day -> m3/s = mm/1000 * area_m2 / 86400
        # Keep as comments for future reference
        "mm_to_m": 1 / 1000.0,
    },
    "paths": {
        # Hard-coded paths — smell
        "forcing": "data/forcing.csv",
        "reaches": "data/reaches.csv",
        "output": "legacy_results.csv",
    },
    # Mixed casing and unclear keys — smell
    "TracerUnits": "mg/L",
    "CatchmentAreaUnits": "km2",
}
