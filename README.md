# embedded-ci-lab

`embedded-ci-lab` is a small Python-based experiment in building a simple CI-like pipeline runner for local development and embedded Linux-oriented workflows.

The project is intentionally minimal. It focuses on clear CLI behavior, config-as-code pipeline definitions, predictable failure handling, and a clean path toward richer reporting and embedded-style CI scenarios.

## Motivation

This project is a hands-on learning exercise focused on CI tooling for embedded Linux workflows.

Modern embedded platforms rely on reproducible build pipelines, configuration-driven tooling, and fast feedback for developers. In embedded and automotive environments, CI is not limited to running unit tests. It often includes validating build configurations, orchestrating Linux-based build steps, handling failures predictably, and preparing the ground for reporting, monitoring, and more advanced integration flows.

`embedded-ci-lab` is intentionally small, but it is designed around the same engineering themes that appear in real embedded integration environments:

- Python-based tooling for developer and CI use cases.
- Linux-oriented command execution and debugging.
- Config-as-code pipeline definitions in YAML.
- Fail-fast execution behavior for clearer diagnostics.
- A path toward structured reporting, observability, and mock embedded build flows.

The longer-term goal is to evolve this project toward a more realistic embedded CI playground with:

- JSON execution reports and basic metrics.
- Richer diagnostics and logging.
- Mock Yocto/BitBake-style pipelines.
- Optional QEMU-based smoke-test stages.
- Cloud-connected artifact or monitoring experiments.

This repository is therefore less about building a generic task runner and more about practicing the design of small, reliable CI building blocks that are relevant to embedded Linux workflows.

## Overview

The tool currently supports:

- Defining pipelines as YAML configuration files.
- Loading pipeline definitions into typed Python models.
- Validating pipeline structure from the CLI.
- Sequentially executing steps using the local shell.
- Stopping on the first non-zero exit code.
- Generating JSON execution reports with pipeline-level and step-level results.
- Showing simple progress output during execution.

This project is designed as a step-by-step learning build. Each feature is introduced in a small, testable increment so the codebase stays understandable and easy to evolve.

## Features

Implemented today:

- CLI skeleton and installable package structure.
- YAML pipeline loading with `yaml.safe_load`.
- `Pipeline` and `Step` typed models.
- `StepResult` and `PipelineResult` execution result models.
- `validate` command for structural pipeline checks.
- `run` command for sequential step execution.
- Fail-fast pipeline behavior.
- JSON execution reports in `reports/`.
- Automated tests for loading, validation, execution, and reporting.

Planned next steps:

- Plain-text or structured logging.
- Timeout handling.
- Retry handling.
- Mock embedded build pipelines.
- Optional Yocto/QEMU-oriented demos.
- Lightweight metrics or observability experiments.

## Project structure

```text
embedded-ci-lab/
├── GEMINI.md
├── PROJECT_PLAN.md
├── PROMPTS.md
├── README.md
├── pyproject.toml
├── embedded_ci_lab/
│   ├── __init__.py
│   ├── cli.py
│   ├── loader.py
│   ├── models.py
│   ├── reporting.py
│   └── runner.py
├── pipelines/
│   ├── demo.yaml
│   ├── success_demo.yaml
│   ├── fail_demo.yaml
│   ├── invalid_empty_name.yaml
│   ├── invalid_no_steps.yaml
│   ├── invalid_empty_command.yaml
│   └── invalid_empty_step_name.yaml
├── reports/
└── tests/
    ├── test_loader.py
    ├── test_runner.py
    └── test_reporting.py
```

## Requirements

- Python 3.11 or newer.
- A local shell environment where pipeline commands can be executed.
- PyYAML for reading YAML pipeline files.

## Installation

Create and activate a virtual environment if you want isolation, then install the project in editable mode:

```bash
pip install -e .
```

Editable installs are convenient during development because changes in the working tree are immediately reflected without reinstalling the package each time.

## Pipeline format

Pipelines are defined as YAML files. A minimal example:

```yaml
pipeline:
  name: Demo Pipeline
  steps:
    - name: Echo Hello
      command: echo Hello
    - name: List Files
      command: dir
```

Current structural expectations:

- `pipeline.name` must exist and must not be empty.
- `pipeline.steps` must contain at least one step.
- Each step must define:
  - `name`
  - `command`

YAML is loaded with `yaml.safe_load`.

## Basic usage

### Validate a pipeline

Use the `validate` command to check pipeline structure before execution:

```bash
embedded-ci validate --pipeline pipelines/demo.yaml
```

Validation checks currently include:

- pipeline file exists,
- YAML is readable,
- pipeline name is present and non-empty,
- at least one step exists,
- each step has a non-empty `name` and `command`.

On success, the command exits with code `0`. On validation failure, it returns a non-zero exit code and prints a clear error message.

### Run a pipeline

Use the `run` command to execute steps sequentially:

```bash
embedded-ci run --pipeline pipelines/success_demo.yaml
```

Example output:

```text
Starting pipeline: Successful Demo Pipeline

[1/2] Echo Hello ... OK
[2/2] List Files ... OK

Pipeline 'Successful Demo Pipeline' completed with status: success.
Report generated: reports\20260606185831_successful_demo_pipeline.json
```

If a step fails, execution stops immediately:

```bash
embedded-ci run --pipeline pipelines/fail_demo.yaml
```

Example output:

```text
Starting pipeline: Failing Demo Pipeline

[1/3] First Step (OK) ... OK
[2/3] Second Step (FAIL) ... FAIL
Command 'exit 1' failed with exit code 1

Pipeline 'Failing Demo Pipeline' completed with status: failure.
Report generated: reports\20260606185831_failing_demo_pipeline.json
```

Current execution behavior:

- steps run one by one,
- a non-zero exit code stops the pipeline,
- the CLI returns `0` for success and `1` for failure,
- a JSON report is written to `reports/` after each run.

## Report format

Each pipeline run generates a JSON report containing pipeline-level and step-level execution metadata.

Top-level fields include:

- `pipeline_name`
- `started_at`
- `finished_at`
- `status`
- `steps`

Each step report includes:

- `name`
- `command`
- `status`
- `exit_code`
- `started_at`
- `finished_at`
- `duration_seconds`
- `stdout`
- `stderr`

Example:

```json
{
  "pipeline_name": "Successful Demo Pipeline",
  "started_at": "2026-06-06T18:58:31.123456",
  "finished_at": "2026-06-06T18:58:31.789012",
  "status": "success",
  "steps": [
    {
      "name": "Echo Hello",
      "command": "echo Hello from successful pipeline",
      "status": "success",
      "exit_code": 0,
      "started_at": "2026-06-06T18:58:31.150000",
      "finished_at": "2026-06-06T18:58:31.250000",
      "duration_seconds": 0.1,
      "stdout": "Hello from successful pipeline\n",
      "stderr": ""
    }
  ]
}
```

## Development workflow

This repository is being developed incrementally using a feature-by-feature workflow.

The rough progression is:

1. Project skeleton.
2. YAML loading.
3. Validation command.
4. Sequential runner.
5. JSON reporting.
6. Logging.
7. Timeouts.
8. Retries.
9. Embedded-oriented pipeline scenarios.

The goal is to keep each step small enough to review, test, and reason about independently.

## Testing

Run the full test suite with:

```bash
pytest
```

You can also run targeted tests, for example:

```bash
pytest tests/test_loader.py
pytest tests/test_runner.py
pytest tests/test_reporting.py
```

The current tests cover:

- valid and invalid YAML loading,
- structural validation scenarios,
- successful sequential execution,
- fail-fast behavior when a step returns a non-zero exit code,
- JSON report generation and report structure.

## Current status

Implemented:

- installable Python CLI package,
- YAML config loading,
- structural validation,
- sequential local execution,
- progress output,
- JSON execution reports in `reports/`,
- automated tests.

Not implemented yet:

- log files,
- timeout handling,
- retry logic,
- parallel execution,
- artifact publishing,
- real Yocto or QEMU integration.

## Why this direction

This project is intentionally biased toward CI building blocks that could later support embedded Linux development workflows.

The Yocto Project provides tools and processes for building custom Linux-based systems for embedded targets, while QEMU can emulate full systems for development and testing. That makes them natural future integration points for a CI playground built around configuration, orchestration, and predictable execution.

## Future work

Planned areas for future exploration:

- Add structured or plain-text logging.
- Add per-step timeout support.
- Add retry support for flaky steps.
- Create mock BitBake-style or Yocto-inspired pipelines.
- Explore QEMU-based smoke tests for emulated targets.
- Experiment with lightweight cloud-backed artifacts or observability.

## Notes

This project is currently aimed at local development and learning. It is not intended yet as a production-grade CI system.

The emphasis is on readability, small steps, and clear behavior first. More advanced capabilities will be added only after the minimal core remains simple and well-tested.