# embedded-ci-lab

`embedded-ci-lab` is a Python-based experiment in building a reliable CI-like pipeline runner, designed for local development and embedded Linux workflows.

## Table of Contents

- [Portfolio Highlights](#portfolio-highlights)
- [Motivation](#motivation)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Local Development & CI](#local-development--ci)
- [Engineering Decisions](#engineering-decisions)
- [Project structure](#project-structure)
- [Future Work](#future-work)

## Portfolio Highlights

This project serves as a showcase of CI/CD engineering fundamentals tailored to an embedded Linux context. It focuses on building reliable, observable, and maintainable automation tools.

### Why this project matters
It demonstrates the transition from simple script-based automation to a structured, reliable CI framework that provides actionable diagnostics.

### Skills demonstrated
- **Reliability Engineering**: Implementation of fail-fast behavior, per-step timeouts, and retry logic.
- **Observability**: Structured logging and generation of JSON execution reports and Prometheus-style metrics.
- **Maintainability**: Strict code quality standards using `ruff`, `mypy`, and `pytest`.
- **DevOps Readiness**: Containerization (Docker) and CI/CD workflow automation.

## Motivation

Modern embedded platforms rely on reproducible build pipelines, configuration-driven tooling, and fast feedback for developers. This project is a hands-on learning exercise focused on designing small, reliable CI building blocks. The goal is to practice engineering themes critical in embedded/automotive environments: fail-fast execution, structured reporting, and reproducible environments.

## Features

- **YAML Pipeline Definitions**: Configuration-as-code.
- **Fail-Fast Execution**: Sequential runner that stops at the first failure.
- **Robustness**: Support for per-step `timeout_seconds` and `retries`.
- **Observability**:
  - Structured **JSON execution reports** (`reports/`).
  - **Structured logging** to stdout and `logs/latest.log`.
  - **Prometheus-style metrics** for monitoring resource usage.
- **Quality Assurance**:
  - Automated `pytest` suite.
  - Static analysis (`ruff`, `mypy`).
  - GitHub Actions CI on all branches.
- **DevOps Ready**: Docker containerization.

## Getting Started

### Prerequisites
- Python 3.11+
- Make (optional, for convenience targets)

### Installation
```bash
pip install -e .[dev]
```

## Usage

### Validate a pipeline
```bash
embedded-ci validate --pipeline pipelines/demo.yaml
```

### Run a pipeline
```bash
embedded-ci run --pipeline pipelines/success_demo.yaml
```

### Run with Docker
```bash
# Build
docker build -t embedded-ci .
# Run
docker run --rm -v $(pwd)/pipelines:/app/pipelines embedded-ci run --pipeline /app/pipelines/success_demo.yaml
```

## Local Development & CI

We use a `Makefile` to simplify common tasks:

```bash
make full-check
```

This runs:
1. Editable installation (`pip install -e .[dev]`)
2. `ruff` (linting)
3. `mypy` (type checking)
4. `pytest` (tests)
5. Pipeline validation & smoke tests

## Engineering Decisions

During development, I prioritized reliability and maintainability:

- **Gitflow**: Used strictly to manage release cycles (`main`, `develop`, `release/*`).
- **Static Analysis**: Enforced `mypy` and `ruff` from the start to ensure code quality and type safety.
- **Fail-Fast**: The runner stops immediately on failure (with retry support) to save resources in embedded build environments.
- **Structured Data**: Used `dataclasses` and `PipelineResult` for reporting to ensure data is predictable and easy to consume by downstream tools.
- **Logging vs. Stdout**: Decoupled output logic using `logging` to support both user feedback (stdout) and persistent diagnostics (`logs/`).

## Project structure

```text
embedded-ci-lab/
├── .github/workflows/ci.yml
├── .gitignore
├── CHANGELOG.md
├── Dockerfile
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

## Future Work

- Parallel step execution.
- Real Yocto/BitBake integration.
- Artifact publishing.
- Cloud-native monitoring/metrics (Prometheus/Grafana).
