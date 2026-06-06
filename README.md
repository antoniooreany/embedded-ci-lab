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

This repository is therefore less about building a generic task runner and more about practicing the design of small, reliable CI building blocks that are relevant to embedded Linux workflows. The Yocto Project is widely used to build custom embedded Linux systems, and QEMU provides full-system emulation that is useful for test and validation scenarios in this kind of environment. [web:292][web:276][web:281]

## Overview

The tool currently supports:

- Defining pipelines as YAML configuration files.
- Loading pipeline definitions into typed Python models.
- Validating pipeline structure from the CLI.
- Sequentially executing steps using the local shell.
- Stopping on the first non-zero exit code.
- Showing simple progress output during execution.

This project is designed as a step-by-step learning build. Each feature is introduced in a small, testable increment so the codebase stays understandable and easy to evolve.

## Features

Implemented today:

- CLI skeleton and installable package structure.
- YAML pipeline loading with `yaml.safe_load`.
- `Pipeline` and `Step` typed models.
- `validate` command for structural pipeline checks.
- `run` command for sequential step execution.
- Fail-fast pipeline behavior.
- Basic demo pipelines for successful and failing runs.
- Automated tests for loading, validation, and execution. [web:209][web:123]

Planned next steps:

- JSON execution reports in `reports/`.
- Step timing and execution metadata.
- Plain-text or structured logging.
- Timeout and retry handling.
- Mock embedded build pipelines.
- Optional Yocto/QEMU-oriented demos. [web:292][web:281]

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
    └── test_runner.py
```

## Requirements

- Python 3.11 or newer.
- A local shell environment where pipeline commands can be executed.
- PyYAML for reading YAML pipeline files. [web:123][web:215]

## Installation

Create and activate a virtual environment if you want isolation, then install the project in editable mode:

```bash
pip install -e .
```

Editable installs are convenient during development because changes in the working tree are immediately reflected without reinstalling the package each time. [web:285][web:287]

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

YAML is loaded with `yaml.safe_load`, which is the recommended safer option for reading YAML input into simple Python objects. [web:209][web:123]

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

Pipeline 'Successful Demo Pipeline' completed successfully.
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
```

Current execution behavior:

- steps run one by one,
- a non-zero exit code stops the pipeline,
- the CLI returns `0` for success and `1` for failure.

## Development workflow

This repository is being developed incrementally using a feature-by-feature workflow.

The rough progression is:

1. Project skeleton.
2. YAML loading.
3. Validation command.
4. Sequential runner.
5. Reporting.
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
```

The current tests cover:

- valid and invalid YAML loading,
- structural validation scenarios,
- successful sequential execution,
- fail-fast behavior when a step returns a non-zero exit code.

## Current status

Implemented:

- installable Python CLI package,
- YAML config loading,
- structural validation,
- sequential local execution,
- progress output,
- automated tests.

Not implemented yet:

- JSON reports,
- log files,
- timeout handling,
- retry logic,
- parallel execution,
- artifact publishing,
- real Yocto or QEMU integration.

## Why this direction

This project is intentionally biased toward CI building blocks that could later support embedded Linux development workflows.

The Yocto Project provides tools and processes for building custom Linux-based systems for embedded targets, while QEMU can emulate full systems for development and testing. That makes them natural future integration points for a CI playground built around configuration, orchestration, and predictable execution. [web:281][web:276][web:292]

## Future work

Planned areas for future exploration:

- Generate JSON execution reports in `reports/`.
- Add timestamps, durations, and per-step execution metadata.
- Introduce logging with cleaner diagnostics.
- Add per-step timeout support.
- Add retry support for flaky steps.
- Create mock BitBake-style or Yocto-inspired pipelines.
- Explore QEMU-based smoke tests for emulated targets.
- Experiment with lightweight cloud-backed artifacts or observability.

## Notes

This project is currently aimed at local development and learning. It is not intended yet as a production-grade CI system.

The emphasis is on readability, small steps, and clear behavior first. More advanced capabilities will be added only after the minimal core remains simple and well-tested.