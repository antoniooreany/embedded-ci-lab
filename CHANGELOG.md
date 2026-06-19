# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.1] - 2026-06-19

### Documentation
- **TOC Correction**: Fixed anchor links for integration scenarios in `README.md` to ensure correct section navigation.
- **Yocto/BitBake Ecosystem Documentation**: Clarified demo output expectations, streamlined manual build steps, and added a directory structure diagram for WSL2 environments to simplify developer onboarding.
- **Header Alignment**: Renamed the section to "Yocto/BitBake Integration Ecosystem" for visual and thematic consistency.

## [2.3.0] - 2026-06-17

### Added
- **Full Yocto Integration**: Successfully orchestrated and verified a real-world 4,000+ task BitBake build cycle.
- **Automated Metadata Management**: Implemented `yocto_init.sh` to automate environment preparation, layer injection, and `IMAGE_INSTALL` configuration.
- **CLI Enhancements**: Added support for the `--version` flag.

### Fixed
- **Pipeline Stability**: Refactored shell logic into standalone scripts to resolve quoting and environment persistence issues in CI/WSL2.
- **Path Portability**: Generalized all pipeline and documentation paths using `${HOME}` to support cross-environment execution.
- **Dependency Management**: Pinned `hypothesis` and updated build tools to ensure deterministic installation and avoid PEP 660 hook errors.

### Documentation
- **UX Restructure**: Overhauled `README.md` with a "Demo First" approach, prioritizing immediate project value and Rapid Demos.
- **Onboarding Reliability**: Added comprehensive WSL2 advisories (Native FS requirements, `chmod` permissions) and explicit setup commands.

## [2.2.1] - 2026-06-15

### Added
- **Visual Architecture Diagram**: Integrated a professional Mermaid.js diagram in `README.md` to visualize the CI/CD integration and framework execution flow.
- **Unified Documentation**: Consolidated all Yocto/BitBake integration content under a cohesive header for improved navigability.
- **Strategic Roadmap**: Added a "Future Work" section outlining prioritized goals for security, scalability, and developer experience.

### Fixed
- **Cross-project Linking**: Updated and corrected reference links to the companion `yocto-lab` repository.
- **Documentation Accuracy**: Refined the project structure tree and corrected `ARTIFACTS_ROOT` paths in examples.

## [2.2.0] - 2026-06-14

### Added
- **Real-world Yocto Build Pipeline**: Added `pipelines/integration/real_yocto_build.yaml` which performs a full BitBake build with custom layer injection and resource monitoring.
- **Hardware-Aware Resource Limits**: Configured memory guarding specifically for high-performance development workstations.
- **Documentation**: Added comprehensive "Real-world Yocto Build Guide" with setup prerequisites, dependency management, and troubleshooting steps.
- **Testing**: Added end-to-end regression tests to verify the full Yocto build lifecycle orchestration.

## [2.1.2] - 2026-06-13

### Documentation
- Expanded the "Project structure" section in `README.md` to include detailed file listings for `pipelines/core/` and `pipelines/integration/`.
- Updated all pipeline path references in `README.md` and simplified command examples by removing redundant cross-platform duplication.
- Clarified cross-platform Docker usage instructions in `README.md` for Windows PowerShell (`${PWD}` vs `$(pwd)`).

## [2.1.1] - 2026-06-13

### Added
- **Test Suite Refactoring**: Renamed E2E test files for architectural clarity and consistent naming conventions.

## [2.1.0] - 2026-06-12

### Added
- **Integration Testing**: Added end-to-end regression tests for Yocto CI scenarios (`tests/test_integration.py`).
- **Robustness Testing**: Introduced property-based tests using `hypothesis` and concurrency tests for report generation in `tests/test_robustness.py`.
- **CI Reliability**: Added missing `hypothesis` dependency in `pyproject.toml` to ensure CI pipeline stability.
- **Documentation**: Streamlined README by applying the DRY principle, removing redundant scenario descriptions, and fixing stale pipeline references.

## [2.0.0] - 2026-06-11

### Added
- **Robust Env Var Substitution**: Pipelines now support Bash-style default values for environment variables (e.g., `${VAR:-default}`).
- **Cross-Platform Readiness**: Enhanced documentation with explicit Windows (PowerShell) and Linux (Bash) examples.
- **Portability**: Unifed all artifact path configurations to use `artifacts_root` consistently across YAML, Python, and environment variables.
- **Integration**: Verified full compatibility with the companion `yocto-lab` repository (v0.3.1).

### Fixed
- **Runner Stability**: Resolved missing `os` import and inconsistent parameter naming in the execution engine.
- **Artifact Validation**: Ensured reliable path resolution using `Path.resolve()` for external repository validation.

## [1.0.0] - 2026-06-10

### Added
- **Yocto-Oriented CI Readiness**: Finalized support for Yocto artifact validation, memory/resource guarding, and Zuul-style integration concepts.
- **Portfolio Polish**: Unified documentation and standards across the project.
- **Regression Suite**: Full backward-compatibility coverage for shell-based pipelines.
- **Yocto Lab Integration**: Added a real-world sanity check pipeline (`pipelines/yocto_policy_gate_fail.yaml`) that validates the structure of the companion `yocto-lab` repository.
- **Recursive Validation**: Upgraded Yocto artifact validator to support recursive discovery and flexible pattern matching (e.g., `meta-*/conf/layer.conf`).

### Fixed
- **Artifact Validation**: Used `Path.resolve()` in `yocto_validator.py` to ensure reliable relative path handling in CI environments, fixing path resolution errors when validating external repositories.

## [0.9.0] - 2026-06-08

### Added
- **Engineering Standards**: Adopted MIT License.
- **Automated Quality Gates**: Integrated `.pre-commit-config.yaml` with Ruff and MyPy.
- **Portfolio Readiness**: Added visual badges for license, Python version, and build status.

## [0.8.1] - 2026-06-08

### Added
- **Portfolio Polish**: Finalized README cross-linking with the companion `yocto-lab` repository.
- **Consistency**: Unified the portfolio narrative across both repositories to clearly distinguish between CI tooling and domain-learning sandbox.

## [0.8.0] - 2026-06-08

### Added
- **Portfolio Positioning**: Restructured README to explicitly position the project as CI/CD tooling for embedded Linux and Yocto-oriented build environments.
- **Regression Suite**: Added comprehensive backward-compatibility tests to ensure the stability of the core shell execution and reporting logic.

## [0.7.0] - 2026-06-08

### Added
- **Resource Guards**: Implemented per-step memory limits (`memory_limit_mb`) to prevent resource exhaustion on CI agents.
- **Memory Warnings**: Introduced optional "soft limits" (`memory_warn_mb`) that trigger alerts in logs and reports without failing the pipeline.
- **Enhanced Reporting**: Execution reports and Prometheus metrics now include step-level warnings and peak memory usage details.

## [0.6.0] - 2026-06-08

### Added
- **Yocto Artifact Validation**: Dedicated step type `yocto_validate_artifacts` to verify build outputs (kernel, rootfs, manifests).
- **Yocto Demo Pipelines**: Added `pipelines/yocto_validate_demo.yaml` and failure scenarios.
- **Validation Fixtures**: Added sample artifact placeholders in `tests/fixtures/yocto_artifacts/` for reproducible testing.

### Changed
- **Pipeline Model**: Extended `Step` with `type` field (defaults to `shell`) and support for step-specific parameters.

## [0.5.0] - 2026-06-07

### Added
- **Resource Metrics Export**: Pipeline execution now captures memory usage (`max_memory_mb`) and duration, exporting them in Prometheus text format (`reports/latest_metrics.prom`).
- **Resource Monitoring**: Enhanced `runner.py` to recursively monitor memory usage of all child processes using `psutil`.

## [0.4.0] - 2026-06-07

### Added
- Logging for pipeline execution (step progress and final status).
- Step timeouts and retries support.
- New demo pipeline `pipelines/yocto-demo.yaml` simulating a Yocto build flow.

## [0.3.0] - 2026-06-07

### Added
- **Docker Support**: Added Dockerfile and .dockerignore for containerized execution.

## v0.2.0 - 2026-06-07

### Added
- **Pipeline Logging**: Logs pipeline execution to stdout and `logs/latest.log`.
- **Step Timeouts & Retries**: Core support for execution limits.

## v0.1.0 - 2026-06-06

### Added
- **Core CLI**: Initial Python CLI with `run` and `validate`.
- **YAML Pipeline Loader**: Support for sequential execution and JSON reporting.
