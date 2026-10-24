# Current handoff

## Goal
Fix the importer so relative source paths are preserved.

## Completed and verified
- Added a regression for nested Markdown paths.

## Open work
- Verify the command from a clean Python 3.11 environment.

## Decisions and constraints
- Use only Python's standard library.
- Do not read files outside the selected example directory.

## Checks run
- `python3 -m unittest discover -s tests -q` — 8 passed, run recorded by the example author.

## Next action
Run the suite again after the packaging check. These notes are synthetic and the test status is illustrative, not a claim about this repository.
