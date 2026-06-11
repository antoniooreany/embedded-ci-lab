# CHANGELOG

## [2.0.0] - 2026-06-11

### Added
- **Robust Env Var Substitution**: Pipelines now support Bash-style default values for environment variables (e.g., `${VAR:-default}`).
- **Cross-Platform Readiness**: Enhanced documentation with explicit Windows (PowerShell) and Linux (Bash) examples.
- **Portability**: Unifed all artifact path configurations to use `artifacts_root` consistently across YAML, Python, and environment variables.

### Fixed
- **Runner Stability**: Resolved missing `os` import and inconsistent parameter naming in the execution engine.
- **Artifact Validation**: Ensured reliable path resolution using `Path.resolve()` for external repository validation.

## [1.0.0] - 2026-06-10

### Added
- **Yocto-Oriented CI Readiness**: Support for artifact validation, memory guards, and Prometheus metrics.
- **Portfolio Polish**: Unified documentation and regression suite.
- **Yocto Lab Integration**: Real-world sanity check pipeline for external metadata.

## [0.9.0] - 2026-06-08

### Added
- MIT License and Quality Gates (Ruff/MyPy).

## [0.1.0] - 2026-06-06

### Added
- Initial release with Core CLI and YAML loading.
