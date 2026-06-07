# CHANGELOG

## [0.5.0] - 2026-06-07

### Added
- **Resource Metrics Export**: Pipeline execution now captures memory usage (`max_memory_mb`) and duration, exporting them in Prometheus text format (`reports/latest_metrics.prom`).
- **Resource Monitoring**: Enhanced `runner.py` to recursively monitor memory usage of all child processes using `psutil`.

## [0.4.0] - 2026-06-07

### Added
- **Resource Metrics Export**: Pipeline execution now captures memory usage (`max_memory_mb`) and duration, exporting them in Prometheus text format (`reports/latest_metrics.prom`).
- **Resource Monitoring**: Enhanced `runner.py` to recursively monitor memory usage of all child processes using `psutil`.

## [0.3.0] - 2026-06-07

### Added
- Logging for pipeline execution (step progress and final status).
- Step timeouts to prevent long-hanging commands.
- Step retries with configurable retry count per step.
- New demo pipeline `pipelines/yocto-demo.yaml` simulating a future Yocto/BitBake flow.
- Documentation updates for installation, validation, running pipelines, and report/log locations.

### Changed
- Internal refactors to keep clear module boundaries (cli, models, loader, runner, reporting) without behavior changes.

## v0.2.0 - 2026-06-07

### Added

-   **Pipeline Logging**: Logs pipeline execution to stdout and `logs/latest.log`.
-   **Step Timeouts**: Support for `timeout_seconds` field in pipeline steps to prevent long-running commands.
-   **Step Retries**: Support for `retries` field in pipeline steps to handle transient failures.
-   **CI Workflow**: Updated GitHub Actions to run tests on all branches and PRs.

### Fixed

-   Adapted runner tests to use `caplog` for reliable verification of logging output.
-   Fixed Python syntax errors in retry-related test commands.

## v0.1.0 - 2026-06-06

### Added

-   **Core CLI**: Initial Python CLI with `run` and `validate` commands.
-   **YAML Pipeline Loader**: Support for defining pipelines in YAML files (`pipelines/`).
-   **Pipeline Models**: `Pipeline` and `Step` dataclasses for structured definition.
-   **Pipeline Validation**: `validate` command to check pipeline structure.
-   **Sequential Runner**: `run` command for executing pipeline steps sequentially with fail-fast behavior.
-   **JSON Reporting**: Detailed JSON execution reports (`reports/`).
-   **Automated Tests**: Comprehensive suite for loader, runner, validation, and reporting.
-   **GitHub Actions CI**: Initial CI workflow.
-   **Gitflow Workflow**: Project established with `main`, `develop`, and feature/release branches.

### Changed

-   Updated `pyproject.toml` for project metadata and dependency management.
-   Revised `README.md` to reflect current features and project structure.

### Fixed

-   Initial git history re-aligned to conform strictly to Gitflow.
-   Compatibility fix for `ls` command in demo pipelines.
-   Test assertion updates for `PipelineResult` output.
-   Minor f-string syntax errors in `runner.py`.
-   Integration test fixes.
