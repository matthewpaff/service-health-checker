# Service Health Checker

Evaluate supplied readiness probe results with consecutive success/failure thresholds.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m health_lab --help
python -m health_lab examples/sample.json
python -m health_lab --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Input requires probes, a list of up to 1000 booleans. Optional failure_threshold and success_threshold are integers from 1 to 10, defaulting to 3 and 1; initial_ready is a boolean defaulting to false. State changes after the relevant consecutive threshold is reached, and the opposite streak resets on each probe. Output includes a ready/unready state after each supplied result, final readiness, and current streak lengths. No probes preserves initial readiness. This evaluates explicit mock results only: it makes no network requests, performs no container/process checks, and is not a production monitoring or liveness controller.

## Learning focus

The modeled 2016 deployment and service-health learning themes: mock readiness checks, failure thresholds, and recovery behavior. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `health_lab/core.py`: validated parsing, storage, or state transitions.
- `health_lab/cli.py`: JSON command interface.
- `health_lab/generate_fixtures.py`: original deterministic validation cases.
- `health_lab/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 408 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
