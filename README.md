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
- Logging execution to stdout and a file.
- Per-step timeout and retry configuration.
- Showing simple progress output during execution.

This project is designed as a step-by-step learning build. Each feature is introduced in a small, testable increment so the codebase stays understandable and easy to evolve.

## Features

Implemented:

- CLI skeleton and installable package structure.
- YAML pipeline loading.
- Typed pipeline models.
- Structural pipeline validation.
- Sequential local step execution with fail-fast behavior.
- JSON execution reports.
- Structured logging to stdout and file.
- Per-step timeout and retry handling.
- Automated testing suite.
- GitHub Actions CI.

Planned next steps:

- Parallel execution.
- Artifact publishing.
- Real Yocto/QEMU integration.
- Cloud-native metrics.

## Project structure

```text
embedded-ci-lab/
├── .github/workflows/ci.yml
├── .gitignore
├── CHANGELOG.md
├── Makefile
├── README.md
├── pyproject.toml
├── embedded_ci_lab/
│   ├── cli.py
│   ├── loader.py
│   ├── models.py
│   ├── reporting.py
│   ├── runner.py
│   └── utils.py
├── logs/
├── pipelines/
│   ├── demo.yaml
│   ├── yocto-demo.yaml
│   ├── success_demo.yaml
│   ├── fail_demo.yaml
│   └── retry_demo.yaml
├── reports/
└── tests/
    ├── test_loader.py
    ├── test_logging.py
    ├── test_reporting.py
    ├── test_retries.py
    ├── test_runner.py
    ├── test_skeleton.py
    └── test_timeout.py
```

## Requirements

- Python 3.11 or newer.
- A local shell environment where pipeline commands can be executed.
- PyYAML for reading YAML pipeline files.

## Installation

Create and activate a virtual environment if you want isolation, then install the project in editable mode:

```bash
pip install -e .[dev]
```

Editable installs are convenient during development because changes in the working tree are immediately reflected without reinstalling the package each time.

## Local development checks

```bash
make full-check
```

This runs:
- editable install
- ruff
- mypy
- pytest
- pipeline validation
- demo pipeline smoke tests

## Pipeline format

Pipelines are defined as YAML files. Example with advanced features:

```yaml
name: Demo Pipeline
steps:
  - name: Step 1
    command: echo Hello
    timeout_seconds: 5
  - name: Flaky Step
    command: exit 1
    retries: 2
```

## Basic usage

### Validate a pipeline

```bash
embedded-ci validate --pipeline pipelines/demo.yaml
```

### Run a pipeline

```bash
embedded-ci run --pipeline pipelines/success_demo.yaml
```

## Notes

This project is currently aimed at local development and learning. It is not intended yet as a production-grade CI system.

The emphasis is on readability, small steps, and clear behavior first. More advanced capabilities will be added only after the minimal core remains simple and well-tested.