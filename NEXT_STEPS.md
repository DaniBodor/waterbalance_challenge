NEXT STEPS (for candidates)

Use this file to document:

- Trade-offs you made due to timebox.
- Known limitations or TODOs you would address next.
- Ideas for tests, performance, design layering, or CI enhancements.

Template

- What I finished:
  - refactoring codebase
  - added an additional test for the date parser
- What I would do next if I had more time:
  - figure out how beta comes into the equation (removed for now)
  - for date parser, add an input argument to allow different date formats, rather than forcing a single one and returning error.
  - diagnose whether AI split the `run_all` function up too much into separate modules.
  - add more tests, currently a large part of the code base is still untested
  - fix type checking errors
- Risks/assumptions:
  - ...
- Notes for reviewers:
  - removal of beta not properly documented in code base (it was not actually used before).
  - regarding date parsing: disallowed incorrect date formats rather than (silently) guessing that it is US formatted; this feels safer than allowing it and logging the assumption made.
