# Configuration constants
BETA = 0.85  # recession/baseflow factor (unitless)
MM_TO_M = 1 / 1000.0  # millimeter to meter conversion
MM_DAY_TO_M3_S = (
    1 / 86.4
)  # millimeter/day to cubic meter/second conversion factor for 1 km²

# File paths (consider loading from environment or config file in future)
FORCING_PATH = "data/forcing.csv"
REACHES_PATH = "data/reaches.csv"
OUTPUT_PATH = "data/model_results.csv"

# Units
TRACER_UNITS = "mg/L"
CATCHMENT_AREA_UNITS = "km2"
