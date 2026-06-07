.PHONY: help install lint typecheck test validate pipelines smoke expected-failures full-check clean-reports

help:
	@echo Available targets:
	@echo   install           - install project in editable mode
	@echo   lint              - run ruff
	@echo   typecheck         - run mypy
	@echo   test              - run pytest
	@echo   validate          - validate all demo pipelines
	@echo   smoke             - run success pipelines
	@echo   expected-failures - run pipelines that are expected to fail
	@echo   pipelines         - validate + run all demo pipelines
	@echo   full-check        - install + lint + typecheck + test + pipelines
	@echo   clean-reports     - remove generated reports

install:
	pip install -e .

lint:
	ruff check .

typecheck:
	mypy .

test:
	pytest

validate:
	embedded-ci validate --pipeline pipelines/retry_demo.yaml
	embedded-ci validate --pipeline pipelines/yocto-demo.yaml
	embedded-ci validate --pipeline pipelines/fail_demo.yaml
	embedded-ci validate --pipeline pipelines/timeout_demo.yaml

smoke:
	embedded-ci run --pipeline pipelines/retry_demo.yaml
	embedded-ci run --pipeline pipelines/yocto-demo.yaml

expected-failures:
	@echo Running expected-failure pipelines...
	@cmd /c "embedded-ci run --pipeline pipelines/fail_demo.yaml && (echo ERROR: fail_demo.yaml unexpectedly succeeded & exit /b 1) || (echo OK: fail_demo.yaml failed as expected & exit /b 0)"
	@cmd /c "embedded-ci run --pipeline pipelines/timeout_demo.yaml && (echo ERROR: timeout_demo.yaml unexpectedly succeeded & exit /b 1) || (echo OK: timeout_demo.yaml failed as expected & exit /b 0)"

pipelines: validate smoke expected-failures

full-check: install lint typecheck test pipelines

clean-reports:
	@if exist reports\*.json del /Q reports\*.json