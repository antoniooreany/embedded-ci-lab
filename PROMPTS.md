# embedded-ci-lab — Gemini CLI prompts

Use these prompts in order.  
Do not skip steps.  
After each step, review the diff and confirm the result before moving on.

---

# embedded-ci-lab — Gemini CLI prompts

Project-wide working rules are defined in `GEMINI.md`.
Use the prompts below in order.
Do not skip steps.
After each step, review the diff and confirm the result before moving on.

---

## Stop prompt

```text
Stop. You went beyond the current step.

Roll back mentally to the last completed goal and complete only the current small step.
You must not:
- add new features,
- change architecture without need,
- rewrite already working code,
- add dependencies without a clear reason.

First, list what belongs to the current step and what does not.
Then make only the minimum necessary changes.
At the end, run tests and fix problems.
```

---

## Prompt 1 — plan first

```text
We are creating a new project named embedded-ci-lab.

Your task now:
1. First propose a minimal MVP in 5-8 bullet points.
2. Then create a very simple implementation plan for the first version only.
3. Do not write code yet.
4. Goal of the first version: a Python CLI that reads a YAML pipeline, runs steps sequentially, and writes a JSON report.
5. For now: no Yocto, no GCP, no GitHub Actions. Local MVP only.
6. Use Python 3.11+, pytest, pyyaml, and the standard library.
7. After the plan, ask for confirmation before implementation.

Constraints:
- Do not add unnecessary dependencies.
- Do not build a web UI.
- Do not overengineer the architecture.
- Use clear and simple file and folder names.
```

---

## Prompt 2 — create skeleton

```text
Implement only step 1 of the plan: create the minimal project skeleton for embedded-ci-lab.

Do:
1. Create the project folder structure.
2. Add pyproject.toml.
3. Add README.md with a very short MVP description.
4. Add the embedded_ci_lab package.
5. Add file stubs without extra logic.

Required structure:
- embedded_ci_lab/
- tests/
- pipelines/
- reports/

Requirements:
- Choose either src-layout or flat-layout and stick to one simple approach.
- Add a CLI entry point even if it only prints "embedded-ci-lab".
- Do not implement the pipeline runner yet.

After changes:
a) show the final file structure,
b) run the project locally,
c) run pytest,
d) fix any errors,
e) end with a short report: what was created, which commands were run, whether all tests are green.

Do nothing beyond this step.
```

---

## Prompt 3 — load YAML

```text
Now implement the next small step: basic CLI loading.

Need:
1. Add a CLI command:
   embedded-ci-lab run --pipeline pipelines/demo.yaml
2. For now the command only needs to:
   - check that the file exists,
   - load YAML,
   - print the pipeline name and number of steps.
3. Add a dataclass or simple typed parser for the pipeline structure.
4. Do not execute step commands yet.

Requirements:
- Error messages must be clear.
- Keep the code small and readable.
- Add unit tests for:
  - successful YAML loading,
  - missing file,
  - invalid YAML.

After finishing:
1. run pytest,
2. show test results,
3. fix any failures,
4. show an example CLI run with demo.yaml.
```

---

## Prompt 4 — sequential runner

```text
Implement the next small step: sequential pipeline execution.

Need:
1. Execute commands from YAML one by one.
2. Support step fields:
   - name
   - command
3. Use subprocess.
4. If a step exits with a non-zero exit code, stop the pipeline.
5. Print simple progress output:
   [1/3] step-name ... OK/FAIL

Do not add yet:
- retries
- timeout
- parallel execution
- depends_on

Add tests for:
- a successful pipeline with 2 steps,
- failure on the second step,
- stopping after the first error.

After finishing:
1. run pytest,
2. run the demo pipeline locally,
3. fix any issues,
4. show the expected final output.
```

---

## Prompt 5 — JSON report

```text
Now add JSON reporting for pipeline runs.

Need:
1. Save a JSON file in reports/ after each run.
2. File name format: timestamp + pipeline name.
3. Save in the report:
   - pipeline_name
   - started_at
   - finished_at
   - status
   - steps
4. For each step save:
   - name
   - command
   - status
   - exit_code
   - started_at
   - finished_at
   - duration_seconds

Requirements:
- The JSON format should be stable and easy to understand.
- Separate report logic from CLI as much as possible without overengineering.

Add tests for:
- report file is created,
- report contains the required fields,
- failed pipeline gets status=failed.

After finishing:
1. run pytest,
2. run the demo pipeline,
3. show a sample generated JSON report,
4. fix all issues found.
```

---

## Prompt 6 — validate command

```text
Now improve the DX a little: add a validate command.

Need:
1. CLI command:
   embedded-ci-lab validate --pipeline pipelines/demo.yaml
2. The command should check:
   - file exists,
   - YAML is valid,
   - pipeline.name exists,
   - at least one step exists,
   - each step has name and command.
3. Return exit code 0 on success.
4. Return non-zero exit code and a clear message on failure.

Add tests for:
- valid pipeline,
- empty steps list,
- missing command field,
- missing pipeline name.

After finishing:
1. run pytest,
2. show examples of validate success and failure,
3. fix all problems.
```

---

## Prompt 7 — logging

```text
Now make the project more professional, but still simple: add logging.

Need:
1. Add logging for pipeline runs.
2. Logs should go to stdout and logs/latest.log.
3. For the first stage, plain text logging is enough.
4. Logs should include:
   - pipeline start,
   - step start,
   - step finish,
   - pipeline success/failure.

Do not add yet:
- rotation
- remote logging
- cloud logging

Add tests where practical. If full log testing is awkward, use a light integration-style test to check log file creation and key messages.

After finishing:
1. run pytest,
2. run the demo pipeline,
3. show an example log file,
4. fix all issues.
```

---

## Prompt 8 — timeout

```text
Now add timeout support for step execution.

Need:
1. Support optional YAML field: timeout_seconds.
2. If a command exceeds the timeout, mark the step as failed.
3. Stop the pipeline after a timeout.
4. Show timeout-related failure in the report.

Add tests for:
- normal step without timeout still works,
- step with timeout fails correctly,
- later steps are not executed after timeout.

After finishing:
1. run pytest,
2. create a separate demo pipeline with timeout,
3. show the execution result and report,
4. fix all issues.
```

---

## Prompt 9 — retries

```text
Now add retries, but keep it minimal.

Need:
1. Support optional YAML field: retries.
2. If a step fails, retry it up to N additional attempts.
3. Show the number of attempts in console output and in the report.
4. If one retry succeeds, continue the pipeline.

Do not add:
- backoff
- jitter
- advanced retry policies

Add tests for:
- success without retry,
- failure followed by success on retry,
- failure after all retries are exhausted.

After finishing:
1. run pytest,
2. show a demo pipeline for retries,
3. show the report,
4. fix all issues.
```

---

## Prompt 10 — cleanup refactor

```text
Now do a cleanup and minimal refactor without expanding functionality.

Do:
1. Check whether the code has grown messily.
2. Keep or improve module boundaries:
   - cli
   - models
   - loader
   - runner
   - reporting
3. Do not change behavior.
4. Update README with:
   - how to install,
   - how to validate a pipeline,
   - how to run a pipeline,
   - where reports and logs are stored.

After changes:
1. run pytest,
2. run demo pipelines,
3. show the final project structure,
4. list what changed without behavior changes.
```

---

## Prompt 11 — GitHub Actions

```text
Now add GitHub Actions only for Python tests.

Need:
1. Create a simple workflow:
   - checkout
   - setup-python
   - install project
   - run pytest
2. No matrix.
3. No publishing.
4. No release.

Also do:
- add a badge to README if appropriate,
- add a short CI section in README.

After finishing:
1. check the workflow YAML for obvious problems,
2. show the workflow content,
3. explain how to test it on GitHub,
4. do not add anything beyond test CI.
```

---

## Prompt 12 — mock embedded pipeline

```text
Now prepare the project for the next stage, but do not implement Yocto yet.

Need:
1. Add a sample pipeline file named yocto-demo.yaml.
2. It should not run real bitbake yet.
3. It should simulate a future embedded build flow with steps:
   - validate-config
   - prepare-build-env
   - mock-bitbake-build
   - package-artifacts
4. Add a short "Future work" section to README with:
   - real Yocto/BitBake integration
   - QEMU smoke test
   - artifact publishing
   - cloud metrics

Do not implement future work now.

After finishing:
1. show the new demo pipeline,
2. run validate on it,
3. confirm all tests still pass.
```