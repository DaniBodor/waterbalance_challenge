Deltares Python Developer Take‑Home Test — Tasks

Timebox
- Core: 3–4 hours
- Optional medior extensions: +2–4 hours

Objective
Refactor a small legacy hydrology/water‑quality script into a maintainable package with tests, typing, and CI.

Data
- data/forcing.csv: Daily precipitation (mm/day), evapotranspiration (mm/day), and an optional upstream boundary tracer concentration (mg/L).
- data/reaches.csv: Two reaches (A,B) with area_km2 and initial tracer concentrations.

Core tasks (both Junior & Medior)
1) Refactor legacy code
   - Based on a clean coding standard, and object-oriented way of working.
   - provide clear documentations .
   - A properly configured pyproject.toml with package metadata and dependencies
   - Package must be installable via `poetry install` and importable as `import deltares_model` 
2) Correctness
   - Identify and fix at least one planted defect from legacy_code/ (see tests for hints):
     • Unit conversion bug (mm/day → m^3/s)
     • Tracer mixing bug (should be flow‑weighted mass balance)
   - Add/adjust tests so the bug(s) are caught and fixed.
3) Testing
   - Achieve ≥85% coverage on the refactored core logic (src/deltares_model/).
   - Use parametrized tests or property‑based tests where appropriate.
4) Style & Typing
   - Pass ruff, black, and mypy --strict on src/tests.
   - Tweak pyproject.toml config if needed (but keep it reasonable).
5) Docs
   - Create a new README.md with all the assumptions, equations, and how to run the new refactored package locally and 
     in CI.
6) AI-assisted development (required; ~15–30 min)
   - Log your prompts and key outputs in AI_USAGE.md (kept vs. modified, brief reflection).
   - Add `# AI-ASSIST:` markers near code/tests influenced by AI.
   - Fill in the AI_USAGE.md file.

Medior extensions
1) CLI
   - Implement deltares-model that reads CSVs, runs the model, and writes results.csv with columns: Date,Reach,Q_m3s,C_mgL.
   - Provide --help and basic usage.
   - The CLI should replace the old way of running the model. 
2) CI Enhancements
   - Add a matrix for OS (ubuntu-latest, windows-latest) and Python (3.11, 3.12).
   - Cache Poetry and test artifacts; upload coverage and fail if <85%.
3) Performance
   - Profile on the tiny dataset (e.g., cProfile) and optimize a hotspot. Document before/after timings.
   
Deliverables
- Create a github repo (do not name it any name related to deltares or test) and add the code to it.
- open a pull request and make push you work to the branch incrementally (not all at once) in this pull request.
- once you finish the work merge the pull request to the main branch. 
- So the main branch eventually, should have the refactored codebase in src/ with tests.
- NEXT_STEPS.md describing trade‑offs and future work.
- zip your entire local repo (including the .git inside the repo main directory) and send it to me. 

Hints
- Keep math simple and deterministic.
- Isolate unit conversions and mixing equations into small, testable functions.
- Be explicit about units in variable names and docstrings.
- Using Pydantic in parsing inputs is preferable.
