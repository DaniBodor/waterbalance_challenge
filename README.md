Deltares Python Developer Take‑Home Test

Summary
- Role: Junior/Medior Python Software Developer (Deltares)
- Focus: Refactoring legacy code, CI with Poetry, tests and typing, optional extensions
- Timebox: 3–4 hours core, up to 6–8 hours with optional medior tasks
- Deliverables: Refactored code, passing CI, tests ≥85% coverage (core), docs, NEXT_STEPS.md

Narrative
You inherited a small legacy script that calculates a daily water balance and a conservative tracer concentration across two linked river reaches. It grew organically and now needs refactoring into a maintainable package with tests and CI.

Toy system (two reaches)

  [Catchment] --runoff--> [Reach A] --flow--> [Reach B] --outflow--> (downstream)
                          ^ tracer input A      ^ tracer input B

ASCII diagram

+----------------------+        Q_A         +----------------------+
|   Catchment (P, ET)  |  --------------->  |      Reach A         |
|  area A_km2          |                    |  storage, C_A        |
+----------------------+                    +----------------------+
                                               |
                                             Q_A|           Q_B
                                               v             |
                                           mix to B          v
                                         +----------------------+
                                         |      Reach B         |
                                         |  storage, C_B        |
                                         +----------------------+

Where:
- P = precipitation (mm/day)
- ET = evapotranspiration (mm/day)
- Q_A, Q_B = discharges (m^3/s)
- C_A, C_B = tracer concentrations (mg/L)
- Mass balance uses flow-weighted mixing.

Model equations (brief)
- Simple bucket runoff (daily): runoff_mm = max(P - ET, 0) with a recession factor beta for baseflow.
- Convert mm/day to m^3/s via: Q = runoff_mm/1000 * A_km2*1e6 / 86400.
- Tracer mixing in a reach: C_out = (Q_in*C_in + Q_local*C_local) / (Q_in + Q_local) with conservative mass.

Dataset description
- data/forcing.csv: Daily P, ET, and an optional upstream tracer boundary for ~7 days.
- data/reaches.csv: Two reaches with area_km2 and initial tracer concentrations.

Install
- Requires Python 3.12
- We use Poetry for dependency and environment management.

Setup
1) Install Poetry (https://python-poetry.org/docs/#installation)
2) From the repo root:
   - poetry install
   - poetry run pre-commit install  (optional)

Run the legacy script (for context)
- python -m legacy_code.run_legacy
  This produces legacy_results.csv (intentionally unclear and potentially incorrect).

Run the refactored CLI (target)
- poetry run deltares-model --help
- poetry run deltares-model \
    --forcing data/forcing.csv \
    --reaches data/reaches.csv \
    --out results.csv

Run tests and tools
- poetry run pytest -q --cov
- poetry run ruff check .
- poetry run black --check .
- poetry run mypy --strict src tests

Using AI tools (required)
- You may use AI assistants (ChatGPT, Copilot, etc.) to help in the task.
- Requirements for this exercise:
  - Keep a short log in AI_USAGE.md at the repo root: prompts used, outputs kept vs. modified, and a brief reflection.
  - Add inline markers `# AI-ASSIST:` next to code or tests influenced by AI.
  - Include at least one manual correction or improvement to AI output and explain it in AI_USAGE.md.

Expected output (example)
Date,Reach,Q_m3s,C_mgL
2024-01-01,A,0.142,5.00
2024-01-01,B,0.121,3.33
...

Time expectations
- Core tasks 3–4 hours. If time runs out, focus on core correctness and testing. Leave notes in NEXT_STEPS.md on trade-offs and what you’d do next.

What you will do
- See TASKS.md for the detailed steps (Junior vs Medior tracks).

Accessibility
- Hydrology concepts are briefly explained above. Equations are intentionally simple and commented in the code.
