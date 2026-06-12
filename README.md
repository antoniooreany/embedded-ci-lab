# embedded-ci-lab

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

`embedded-ci-lab` is a Python-based framework designed for building reliable, observable CI automation for embedded Linux and Yocto build workflows.

## Table of Contents

- [Yocto/BitBake Integration Ecosystem](#yoctobitbake-integration-ecosystem)
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

## Yocto/BitBake Integration Ecosystem

> **Engineering Note:** To demonstrate how `embedded-ci-lab` manages real-world build metadata, I developed a companion repository, [yocto-lab](https://github.com/antoniooreany/yocto-lab), which serves as a hands-on learning sandbox for Yocto/BitBake.

This ecosystem highlights my experience with both CI/CD tooling and build system internals:

- **`embedded-ci-lab`** (this repo): Python-based framework for reliable CI automation, observability, and resource-aware execution.
- **`yocto-lab`**: Proof-of-contact with BitBake/Yocto metadata, featuring a custom layer, simple recipes, and build configurations.

**Integration**: `embedded-ci-lab` uses the `yocto_validate_artifacts` step to perform automated "Sanity Checks" on Yocto metadata. While `yocto-lab` is provided as a hands-on learning sandbox, this framework is fully environment-agnostic. You can validate any Yocto-compatible directory structure anywhere on your file system by configuring the `artifacts_root` in your pipeline definition, or by using environment variables (e.g., `${ARTIFACTS_ROOT}`) for maximum portability across different CI/CD environments.

### Workflow Setup (for yocto-lab demo)
For integration tests and demos, ensure `yocto-lab` is cloned in the same parent directory:
```text
/projects/
├── embedded-ci-lab/
└── yocto-lab/
```

### Running the Integration Demo
By default, the demo expects `yocto-lab` to be in the parent directory. You can override this using the `ARTIFACTS_ROOT` environment variable:

```bash
# Option 1: Use the default (../yocto-lab)
embedded-ci run --pipeline pipelines/yocto_lab_integration_demo.yaml

# Option 2: Override with custom path
# On Linux/macOS (Bash):
ARTIFACTS_ROOT=/custom/path/to/artefacts embedded-ci run --pipeline pipelines/yocto_lab_integration_demo.yaml

# On Windows (PowerShell):
$env:ARTIFACTS_ROOT="/custom/path/to/artefacts"; embedded-ci run --pipeline pipelines/yocto_lab_integration_demo.yaml
```

This flexibility is achieved using Bash-style variable expansion (`${ARTIFACTS_ROOT:-../yocto-lab}`) supported natively by our pipeline loader.

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

#### Full Yocto CI Cycle
- **Command**: `embedded-ci run --pipeline pipelines/full_yocto_cycle_demo.yaml`
- **Description**: Orchestrates a complete CI workflow: pre-build metadata validation, a resource-monitored simulated build, post-build artifact verification, and workspace cleanup.
- **Key Features Demonstrated**:
  - **Gating**: Ensures metadata is valid before starting the build.
  - **Active Monitoring**: Triggers memory warnings during the simulated "heavy" build step.
  - **Artifact Verification**: Confirms build outputs (kernel and rootfs) were correctly produced.
  - **Infrastructure Hygiene**: Automatically cleans up temporary build artifacts.

#### Integration Sanity Check
- **Command**: `embedded-ci run --pipeline pipelines/yocto_lab_integration_demo.yaml`
- **Description**: Performs a real-world sanity check against the companion `yocto-lab` repository structure.
- **Expected Result**: This pipeline is designed to **FAIL** with an informative error.
- **Engineering Value**: This intentional failure demonstrates the tool's strict validation of directory structures and naming standards (e.g., detecting `meta-example` vs. `meta-custom`). It proves the framework's ability to act as an automated "inspector" that ensures domain-specific standards are met before proceeding with expensive build tasks.

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
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── Dockerfile
├── LICENSE
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
    ├── test_runner.py, test_timeout.py, test_memory_limits.py, test_regression.py,
    └── test_yocto_validator.py, test_yocto_loader.py, test_yocto_runner.py, test_yocto_fixtures.py
```
