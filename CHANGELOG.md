# CHANGELOG

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
