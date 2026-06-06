# CHANGELOG

## v0.1.0 - 2026-06-06

### Added

-   **Core CLI**: Initial Python CLI with `run` and `validate` commands.
-   **YAML Pipeline Loader**: Support for defining pipelines in YAML files (`pipelines/`).
-   **Pipeline Models**: `Pipeline` and `Step` dataclasses for structured definition.
-   **Pipeline Validation**: `validate` command to check pipeline structure (name, steps, command presence).
-   **Sequential Runner**: `run` command for executing pipeline steps sequentially using `subprocess`.
    -   Includes progress output (e.g., `[1/3] Step Name ... OK`).
    -   Implements fail-fast behavior (stops on first non-zero exit code).
-   **JSON Reporting**: `reporting.py` module to generate detailed JSON execution reports (`reports/`).
    -   Reports include pipeline and step status, start/finish times, duration, exit codes, `stdout`, and `stderr`.
-   **Automated Tests**:
    -   `tests/test_loader.py`: Unit tests for YAML loading and validation.
    -   `tests/test_runner.py`: Unit tests for sequential execution logic.
    -   `tests/test_reporting.py`: Unit and integration tests for JSON reporting.
-   **GitHub Actions CI**: Basic workflow (`.github/workflows/ci.yml`) to run `pytest` on `develop`, `main`, and `release/*` branches for continuous integration.
-   **Gitflow Workflow**: Project established with `main`, `develop`, and feature/release branches following Gitflow.

### Changed

-   Updated `pyproject.toml` for project metadata and dependency management.
-   Revised `README.md` to reflect current features and project structure.

### Fixed

-   Initial git history re-aligned to conform strictly to Gitflow.
-   Compatibility fix for `ls` command in demo pipelines (changed to `dir` for Windows).
-   Test assertion updates in `test_runner.py` and `test_reporting.py` to match `PipelineResult` output.
-   Minor f-string syntax errors in `runner.py`.
-   Integration test in `test_reporting.py` updated to correctly invoke CLI and capture output.

