.PHONY: help install lint typecheck test validate pipelines smoke expected-failures full-check clean-reports docker-build docker-smoke docker-validate docker-run-yocto docker-expected-failures

help:
	@echo Available targets:
	@echo   install                  - install project in editable mode
	@echo   lint                     - run ruff
	@echo   typecheck                - run mypy
	@echo   test                     - run pytest
	@echo   validate                 - validate all demo pipelines
	@echo   smoke                    - run success pipelines
	@echo   expected-failures        - run pipelines that are expected to fail
	@echo   pipelines                - validate + run all demo pipelines
	@echo   full-check               - install + lint + typecheck + test + pipelines
	@echo   clean-reports            - remove generated reports
	@echo   docker-build             - build Docker image
	@echo   docker-smoke             - build image and run basic Docker smoke checks
	@echo   docker-validate          - validate all demo pipelines inside Docker
	@echo   docker-run-yocto         - run yocto demo pipeline inside Docker
	@echo   docker-expected-failures - run expected-failure pipelines inside Docker

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

docker-build:
	docker build -t embedded-ci-lab:local .

docker-smoke: docker-build
	docker run --rm embedded-ci-lab:local --help
	docker run --rm embedded-ci-lab:local validate --pipeline pipelines/yocto-demo.yaml
	docker run --rm embedded-ci-lab:local run --pipeline pipelines/yocto-demo.yaml

docker-validate: docker-build
	docker run --rm embedded-ci-lab:local validate --pipeline pipelines/retry_demo.yaml
	docker run --rm embedded-ci-lab:local validate --pipeline pipelines/yocto-demo.yaml
	docker run --rm embedded-ci-lab:local validate --pipeline pipelines/fail_demo.yaml
	docker run --rm embedded-ci-lab:local validate --pipeline pipelines/timeout_demo.yaml

docker-run-yocto: docker-build
	docker run --rm embedded-ci-lab:local run --pipeline pipelines/yocto-demo.yaml

docker-expected-failures: docker-build
	@echo Running expected-failure pipelines in Docker...
	@cmd /c "docker run --rm embedded-ci-lab:local run --pipeline pipelines/fail_demo.yaml && (echo ERROR: fail_demo.yaml unexpectedly succeeded in Docker & exit /b 1) || (echo OK: fail_demo.yaml failed as expected in Docker & exit /b 0)"
	@cmd /c "docker run --rm embedded-ci-lab:local run --pipeline pipelines/timeout_demo.yaml && (echo ERROR: timeout_demo.yaml unexpectedly succeeded in Docker & exit /b 1) || (echo OK: timeout_demo.yaml failed as expected in Docker & exit /b 0)"