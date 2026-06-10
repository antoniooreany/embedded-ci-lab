# CHANGELOG

## [1.0.0-rc1] - 2026-06-10

### Added
- **Yocto Lab Integration**: Added a real-world sanity check pipeline (`pipelines/yocto_lab_integration_demo.yaml`) that validates the structure of the companion `yocto-lab` repository.
- **Documentation**: Enhanced README with an "Integration Sanity Check" section explaining the value of automated metadata validation and intentional failure scenarios for domain-specific standards enforcement.

## [0.9.1] - 2026-06-08

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
