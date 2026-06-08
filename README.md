# embedded-ci-lab

`embedded-ci-lab` is a Python-based framework designed for building reliable, observable CI automation for embedded Linux and Yocto build workflows.

## Table of Contents

- [Portfolio Highlights](#portfolio-highlights)
- [Motivation](#motivation)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [CI/CD Integration Concept](#cicd-integration-concept)
- [Local Development & CI](#local-development--ci)
- [Engineering Decisions](#engineering-decisions)
- [Project structure](#project-structure)
- [Future Work](#future-work)

## Portfolio Highlights

This project serves as a showcase of CI/CD engineering fundamentals tailored to an embedded Linux context. It focuses on building reliable, observable, and resource-aware automation tools.

### Why this project matters
It demonstrates the transition from simple script-based automation to a structured, reliable CI framework that provides actionable diagnostics for complex build systems.

### Skills demonstrated
- **Reliability Engineering**: Implementation of fail-fast behavior, per-step timeouts, and retry logic.
- **Resource Management**: Active "Resource Guarding" with hard memory limits and warning thresholds to protect build infrastructure.
- **Observability**: Structured logging, detailed JSON execution reports, and Prometheus-style metrics for performance tracking.
- **Maintainability**: Strict code quality standards using `ruff`, `mypy`, and `pytest`.
- **DevOps Readiness**: Containerization (Docker) and CI/CD workflow automation.

### Relevance to embedded CI/CD workflows
In embedded Linux projects (e.g., Yocto/BitBake), build pipelines are long, resource-intensive, and complex. This project mimics the requirements of such environments by:
- **Yocto-oriented Artifact Validation**: Automated checks for build outputs (Kernel images, rootfs, manifests).
- **Active Monitoring**: Tracking and limiting resource usage (memory) during high-load build steps.
- **Gated CI Concepts**: Providing the machine-readable output required for integration into gating systems like Zuul.

## Motivation

Modern embedded platforms rely on reproducible build pipelines, configuration-driven tooling, and fast feedback for developers. This project is a hands-on learning exercise focused on designing small, reliable CI building blocks critical in embedded/automotive environments: fail-fast execution, resource-aware guarding, and structured reporting.

## Features

- **YAML Pipeline Definitions**: Configuration-as-code.
- **Fail-Fast Execution**: Sequential runner that stops at the first failure.
- **Yocto-oriented Validation**: Dedicated `yocto_validate_artifacts` step to verify build outputs.
- **Resource Guards**: Support for per-step `memory_limit_mb` (hard limit) and `memory_warn_mb` (soft limit).
- **Execution Robustness**: Support for per-step `timeout_seconds` and `retries`.
- **Observability**:
  - Structured **JSON execution reports** (`reports/`).
  - **Structured logging** to stdout and `logs/latest.log`.
  - **Prometheus-style metrics** for monitoring resource usage and duration.
- **Quality Assurance**: Automated `pytest` suite, static analysis (`ruff`, `mypy`), and GitHub Actions CI.
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
embedded-ci validate --pipeline pipelines/yocto_validate_demo.yaml
```

### Run a pipeline
```bash
embedded-ci run --pipeline pipelines/yocto_validate_demo.yaml
```

### Demo Scenarios
To see specific features in action:
- **Yocto Artifact Validation**: `embedded-ci run --pipeline pipelines/yocto_validate_demo.yaml`
- **Resource Guards (Memory)**: `embedded-ci run --pipeline pipelines/memory_limit_demo.yaml`
- **Timeouts**: `embedded-ci run --pipeline pipelines/timeout_demo.yaml`
- **Retries**: `embedded-ci run --pipeline pipelines/retry_demo.yaml`

### Run with Docker
```bash
# Build
docker build -t embedded-ci .
# Run
docker run --rm -v $(pwd)/pipelines:/app/pipelines embedded-ci run --pipeline /app/pipelines/yocto_validate_demo.yaml
```

## CI/CD Integration Concept

`embedded-ci-lab` is designed to function as a predictable build runner within larger CI/CD architectures (e.g., GitHub Actions, Zuul). It enables moving beyond simple script execution to structured, resource-aware CI automation:

```text
Zuul CI (Gated Change)
      |
      v
[Containerized Job Agent]
      |
      v
embedded-ci-lab (Run & Validate)
      |--------------------------|
      |                          |
      v                          v
[Yocto/BitBake Build]      [Resource Guards]
      |                          |
      v                          v
[Artifact Validator] <------- [Max RSS Tracking]
      |                          |
      v                          v
JSON Reports + Metrics + Pass/Fail Status
```

- **Standardized Interface**: CLI-based execution and validation make it easy to embed as a containerized step.
- **Resource Awareness**: Built-in memory guards protect CI build nodes from OOM (Out Of Memory) failures and identify leaking build tasks.
- **Structured Diagnostics**: JSON reports and Prometheus metrics provide immediate feedback for build dashboards and long-term trend analysis.

## Local Development & CI

We use a `Makefile` to simplify common tasks:

```bash
make full-check
```

## Engineering Decisions

- **Gitflow**: Used strictly to manage release cycles (`main`, `develop`, `release/*`).
- **Static Analysis**: Enforced `mypy` and `ruff` to ensure code quality and type safety.
- **Fail-Fast & Guarding**: The runner stops immediately on failure or resource exhaustion to save costs in expensive build environments.
- **Decoupled Logic**: Separate modules for validation, execution, and reporting for better testability and maintainability.

## Project structure

```text
embedded-ci-lab/
├── .github/workflows/ci.yml
├── CHANGELOG.md
├── Dockerfile
├── Makefile
├── README.md
├── pyproject.toml
├── embedded_ci_lab/
│   ├── cli.py, loader.py, metrics.py, models.py, reporting.py, runner.py, utils.py, yocto_validator.py
├── logs/
├── pipelines/
├── reports/
└── tests/
    ├── test_loader.py, test_logging.py, test_metrics.py, test_reporting.py, test_retries.py,
    ├── test_runner.py, test_timeout.py, test_memory_limits.py,
    └── test_yocto_validator.py, test_yocto_loader.py, test_yocto_runner.py, test_yocto_fixtures.py
```

## Future Work

- Parallel step execution.
- Real Yocto/BitBake integration layer.
- Artifact publishing (S3/Artifactory).
- Cloud-native monitoring dashboards.
