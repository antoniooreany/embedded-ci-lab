# embedded-ci-lab — Project Plan

## Goal

Build a small Python-based CI pipeline runner that reads pipeline definitions from YAML, executes steps locally, and produces reports.

This project starts as a simple local MVP and is designed to evolve later toward:
- config-as-code pipeline execution,
- CI diagnostics and reporting,
- retry and timeout handling,
- mock embedded build flows,
- eventual Yocto/QEMU experimentation.

## Principles

- Build the smallest working version first.
- Keep the codebase simple and easy to test.
- Add only one feature per step.
- Run tests at the end of every step.
- Avoid unnecessary dependencies and overengineering.
- Keep future embedded/Yocto support in mind, but do not implement it too early.

## MVP scope

The first usable version should support:
- a Python CLI,
- loading a YAML pipeline file,
- validating pipeline structure,
- running steps sequentially,
- stopping on failure,
- generating a JSON execution report,
- basic automated tests.

## Proposed project structure

```text
embedded-ci-lab/
├── GEMINI.md
├── README.md
├── pyproject.toml
├── embedded_ci_lab/
│   ├── __init__.py
│   ├── cli.py
│   ├── models.py
│   ├── loader.py
│   ├── runner.py
│   └── reporting.py
├── pipelines/
│   ├── demo.yaml
│   └── yocto-demo.yaml
├── reports/
├── logs/
└── tests/
    ├── test_loader.py
    ├── test_validate.py
    ├── test_runner.py
    └── test_reporting.py
```

## Step-by-step roadmap

### Step 1 — Project skeleton
Create the repository structure, Python package, pyproject.toml, README, and a minimal CLI entry point.

Definition of done:
- project installs locally,
- CLI starts,
- pytest runs successfully.

### Step 2 — Pipeline loading
Load a YAML pipeline file from disk and parse it into typed Python models.

Definition of done:
- valid YAML loads successfully,
- missing file is handled cleanly,
- invalid YAML produces a clear error,
- tests cover the loader behavior.

### Step 3 — Validate command
Add a CLI validation command for checking pipeline structure before execution.

Definition of done:
- checks pipeline name,
- checks at least one step exists,
- checks each step has name and command,
- returns correct exit codes,
- tests are green.

### Step 4 — Sequential execution
Run pipeline steps in order using subprocess.

Definition of done:
- each step executes in sequence,
- output clearly shows progress,
- non-zero exit code stops the pipeline,
- tests cover success and failure cases.

### Step 5 — JSON reporting
Write a JSON execution report after each run.

Definition of done:
- report saved to reports/,
- includes pipeline status and step details,
- includes timing data,
- tests verify report shape and status handling.

### Step 6 — Logging
Add simple logging to stdout and logs/latest.log.

Definition of done:
- pipeline start/end logged,
- step start/end logged,
- failures logged clearly,
- logging works during normal runs.

### Step 7 — Timeout support
Support optional per-step timeout settings.

Definition of done:
- timeout_seconds can be set per step,
- timed-out step fails the pipeline,
- timeout appears in report,
- tests verify behavior.

### Step 8 — Retry support
Support optional retry count for flaky steps.

Definition of done:
- step retries up to configured amount,
- attempt count is visible,
- success after retry is supported,
- exhausted retries fail pipeline,
- tests are green.

### Step 9 — Cleanup refactor
Refactor only enough to keep the code readable and maintainable.

Definition of done:
- responsibilities are separated by module,
- behavior remains unchanged,
- README is updated,
- tests still pass.

### Step 10 — GitHub Actions test workflow
Add a simple workflow for running pytest on GitHub.

Definition of done:
- workflow installs project,
- workflow runs pytest,
- README documents the CI workflow.

### Step 11 — Mock embedded pipeline
Add a themed example pipeline that mimics an embedded build flow.

Definition of done:
- yocto-demo.yaml validates successfully,
- no real BitBake yet,
- README includes “Future work” section.

## Future work

Later, after the MVP is stable, consider:
- real BitBake or Yocto integration,
- QEMU smoke tests,
- artifact packaging and publishing,
- structured JSON logs,
- metrics export,
- cloud integrations such as GCP artifact storage or monitoring,
- dependency graphs and parallel step execution.