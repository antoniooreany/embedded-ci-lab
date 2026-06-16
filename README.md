# embedded-ci-lab

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

`embedded-ci-lab` is a Python-based framework designed for building reliable, observable CI automation for embedded Linux and Yocto build workflows.

## Table of Contents
- [Portfolio Highlights](#portfolio-highlights)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Yocto/BitBake Integration](#yoctobitbake-integration)
  - [Integration Scenarios (Demos)](#integration-scenarios-demos)
  - [Real-world Yocto Build Guide](#real-world-yocto-build-guide)
- [Project structure](#project-structure)
- [Engineering Decisions](#engineering-decisions)
- [Future Work](#future-work)

## Portfolio Highlights

This project serves as a showcase of CI/CD engineering fundamentals tailored to an embedded Linux context. It focuses on building reliable, observable, and resource-aware automation tools.

### Why this project matters
It demonstrates the transition from simple script-based automation to a structured, reliable CI framework that provides actionable diagnostics for complex build systems.

### Motivation
Modern embedded platforms rely on reproducible build pipelines, configuration-driven tooling, and fast feedback for developers. This project is a hands-on learning exercise focused on designing small, reliable CI building blocks critical in embedded/automotive environments: fail-fast execution, resource-aware guarding, and structured reporting.

### Features
- **YAML Pipeline Definitions**: Configuration-as-code.
- **Fail-Fast Execution**: Sequential runner that stops at the first failure.
- **Yocto-oriented Validation**: Dedicated `yocto_validate_artifacts` step to verify build outputs.
- **Resource Guards**: Support for per-step `memory_limit_mb` (hard limit) and `memory_warn_mb` (soft limit).
- **Execution Robustness**: Support for per-step `timeout_seconds` and `retries`.
- **Observability**: Structured **JSON execution reports**, **Structured logging**, and **Prometheus-style metrics**.

---

## Getting Started

### Prerequisites
- Python 3.11+
- Make (optional, for convenience targets)



---

## Usage

```
### Setup & Prerequisites

Ensure both repositories are cloned in the same parent directory:
```bash
mkdir -p ~/yocto-work && cd ~/yocto-work
git clone https://github.com/antoniooreany/embedded-ci-lab.git
git clone https://github.com/antoniooreany/yocto-lab.git
```

Always ensure you are in the project root directory before running commands:
```bash
cd ~/yocto-work/embedded-ci-lab
```

### Directory structure
```text
~/yocto-work/
├── embedded-ci-lab/
└── yocto-lab/
```

### Installation
```bash
pip install -e .[dev]
```

### Check version
```bash
embedded-ci --version

### Validate a pipeline
```bash
embedded-ci validate --pipeline pipelines/core/retry_demo.yaml
```

### Run a pipeline
```bash
embedded-ci run --pipeline pipelines/core/retry_demo.yaml
```

### Run with Docker
```bash
# Build
docker build -t embedded-ci-lab:local .
# Run
docker run --rm -v $(pwd)/pipelines:/app/pipelines embedded-ci-lab:local run --pipeline /app/pipelines/core/retry_demo.yaml
```

---

## Yocto/BitBake Integration

> **Engineering Note:** To demonstrate how `embedded-ci-lab` manages real-world build metadata, I developed a companion repository, [yocto-lab](https://github.com/antoniooreany/yocto-lab), which serves as a hands-on learning sandbox for Yocto/BitBake.

### Integration Scenarios (Demos)

We provide two primary scenarios to demonstrate the framework's capabilities:

#### 1. Strict Metadata Gating (Defensive Scenario)
- **Goal**: Demonstrate **Policy Enforcement** by blocking builds that don't meet corporate standards.
- **Commands**:
  ```bash
  # Validate (should SUCCEED)
  embedded-ci validate --pipeline pipelines/integration/yocto_policy_gate_fail.yaml
  # Run (should FAIL)
  embedded-ci run --pipeline pipelines/integration/yocto_policy_gate_fail.yaml
  ```

#### 2. Full CI Lifecycle (Orchestration Scenario)
- **Goal**: Demonstrate a successful end-to-end build orchestration with resource monitoring.
- **Commands**:
  ```bash
  # Run (should SUCCEED)
  embedded-ci run --pipeline pipelines/integration/yocto_full_cycle_success.yaml
  ```

### Real-world Yocto Build Guide

#### Prerequisites
1. **Workspace & Repos**: Clone `embedded-ci-lab`, `poky` (branch `scarthgap`), and `yocto-lab`: 
```bash
mkdir -p ~/yocto-work && cd ~/yocto-work
git clone https://github.com/antoniooreany/embedded-ci-lab.git
git clone https://git.yoctoproject.org/git/poky && cd poky && git checkout scarthgap && cd ..
git clone https://github.com/antoniooreany/yocto-lab.git
```
2. **Dependencies**: Install required system packages for BitBake:
```bash 
sudo apt-get update && sudo apt-get install -y gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint xterm python3-subunit mesa-common-dev zstd liblz4-tool
```  
3. **Orchestrator Setup**: Create a virtual environment using Python 3.11+:
```bash
cd ~/yocto-work/embedded-ci-lab
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```
4. **Permissions**: Make the initialization script executable:
```bash
chmod +x pipelines/integration/yocto_init.sh
```

#### Directory structure
```text
~/yocto-work/
├── embedded-ci-lab/
├── poky/
└── yocto-lab/
```

#### Running the Build
```bash
ARTIFACTS_ROOT=~/yocto-work/yocto-lab embedded-ci run --pipeline pipelines/integration/yocto_real_build.yaml
```

#### Testing & Troubleshooting
- **Dry-run**: Modify `yocto_real_build.yaml` to use `bitbake -n core-image-minimal`.
- **"Permission denied"**: If the pipeline fails with a permission error, make the initialization script executable **once** after cloning:
```bash
chmod +x pipelines/integration/yocto_init.sh
```
- **Performance/Deadlocks in WSL2**: **Always** run build operations (BitBake) strictly within your native Linux filesystem (`/home/<user>/...`), never on Windows-mounted directories (`/mnt/c/...`).

---

## Project structure

```text
embedded-ci-lab/
├── .github/workflows/ci.yml
├── embedded_ci_lab/  # Core logic
├── pipelines/        # YAML pipeline definitions
├── tests/            # pytest suite
└── ...
```

## Engineering Decisions

- **Gitflow**: Used strictly to manage release cycles (`main`, `develop`, `release/*`).
- **Static Analysis**: Enforced `mypy` and `ruff`.
- **Fail-Fast & Guarding**: The runner stops immediately on failure or resource exhaustion.
- **Decoupled Logic**: Separate modules for validation, execution, and reporting.

## Future Work

### 1. Security & Compliance
- **SBOM Generation**: Full component traceability (SPDX/CycloneDX).
- **Dependency Security Audit**: Automated vulnerability scanning.

### 2. Scalability & Performance
- **Parallel Execution**: Support for parallel processing of independent pipeline steps.

### 3. Core Architecture & Extensibility
- **Pydantic Schema Validation**: Migration to Pydantic models.
- **Plugin Architecture**: Modular plugin system.
