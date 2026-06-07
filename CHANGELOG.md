# CHANGELOG

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
