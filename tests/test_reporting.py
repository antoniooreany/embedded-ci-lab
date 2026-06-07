import os
import json
import yaml
import subprocess
import sys # Added import
from datetime import datetime, timedelta
from embedded_ci_lab.models import PipelineResult, StepResult
from embedded_ci_lab.reporting import generate_report, sanitize_filename

# Helper to create dummy PipelineResult for testing generate_report
def create_dummy_pipeline_result(
    pipeline_name="Test Pipeline",
    status="success",
    num_steps=2,
    fail_step_index=-1
) -> PipelineResult:
    now = datetime.now()
    started_at = now - timedelta(minutes=5)
    finished_at = now

    step_results = []
    for i in range(num_steps):
        step_name = f"Step {i+1}"
        command = f"echo {i+1}"
        step_status = "success"
        exit_code = 0
        step_started_at = started_at + timedelta(seconds=i*30)
        step_finished_at = step_started_at + timedelta(seconds=20)
        duration = (step_finished_at - step_started_at).total_seconds()
        stdout = f"Output for {step_name}"
        stderr = ""

        if i == fail_step_index:
            step_status = "failure"
            exit_code = 1
            
        step_results.append(StepResult(
            name=step_name,
            command=command,
            status=step_status,
            exit_code=exit_code,
            started_at=step_started_at,
            finished_at=step_finished_at,
            duration_seconds=duration,
            stdout=stdout,
            stderr=stderr
        ))

    return PipelineResult(
        pipeline_name=pipeline_name,
        started_at=started_at,
        finished_at=finished_at,
        status=status,
        step_results=step_results
    )

def test_sanitize_filename():
    assert sanitize_filename("My Pipeline Name!") == "my_pipeline_name"
    assert sanitize_filename(r"Path/With\Slashes:And?Other*Chars") == "path_with_slashes_and_other_chars"
    assert sanitize_filename("  Leading and Trailing Spaces  ") == "leading_and_trailing_spaces"

def test_generate_report_successful(tmp_path):
    reports_dir = tmp_path / "reports"
    pipeline_result = create_dummy_pipeline_result(status="success")
    report_file = generate_report(pipeline_result, str(reports_dir))

    assert os.path.exists(report_file)
    assert reports_dir.name in report_file # Check if it's in the reports directory

    with open(report_file, 'r') as f:
        report_data = json.load(f)

    assert report_data["pipeline_name"] == "Test Pipeline"
    assert report_data["status"] == "success"
    assert "started_at" in report_data
    assert "finished_at" in report_data
    assert len(report_data["steps"]) == 2
    assert report_data["steps"][0]["status"] == "success"
    assert report_data["steps"][0]["exit_code"] == 0
    assert "duration_seconds" in report_data["steps"][0]
    assert "stdout" in report_data["steps"][0]
    assert "stderr" in report_data["steps"][0]

def test_generate_report_failing(tmp_path):
    reports_dir = tmp_path / "reports"
    pipeline_result = create_dummy_pipeline_result(status="failure", fail_step_index=0)
    report_file = generate_report(pipeline_result, str(reports_dir))

    assert os.path.exists(report_file)

    with open(report_file, 'r') as f:
        report_data = json.load(f)

    assert report_data["pipeline_name"] == "Test Pipeline"
    assert report_data["status"] == "failure"
    assert report_data["steps"][0]["status"] == "failure"
    assert report_data["steps"][0]["exit_code"] == 1

# Integration test: run a small pipeline and verify report is generated
def test_cli_run_generates_report(tmp_path, capsys):
    # Create a dummy pipeline file
    pipeline_content = {
        "name": "Integration Test Pipe",
        "steps": [
            {"name": "Int Step 1", "command": "echo 'Hello from integration'"}
        ]
    }
    pipeline_file = tmp_path / "integration_pipe.yaml"
    pipeline_file.write_text(yaml.dump(pipeline_content))

    # Temporarily change current working directory to tmp_path to simulate CLI execution
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Call the main function of the CLI directly (or subprocess if needed)
        # Note: If main() uses sys.exit(), direct call will exit the test runner.
        # For this test, it's safer to use subprocess to mimic actual CLI.
        result = subprocess.run(
            [sys.executable, "-m", "embedded_ci_lab.cli", "run", "--pipeline", str(pipeline_file)],
            capture_output=True,
            text=True,
            check=False # Do not raise exception on non-zero exit code
        )
        cli_output = result.stdout + result.stderr
        
        assert "Pipeline 'Integration Test Pipe' completed with status: success." in cli_output
        assert "Report generated:" in cli_output
        
        # Verify the report file exists
        reports_dir = tmp_path / "reports"
        report_files = list(reports_dir.glob("*.json"))
        assert len(report_files) == 1
        
        # Basic check of report content
        with open(report_files[0], 'r') as f:
            report_data = json.load(f)
            assert report_data["pipeline_name"] == "Integration Test Pipe"
            assert report_data["status"] == "success"
            assert len(report_data["steps"]) == 1
            assert report_data["steps"][0]["name"] == "Int Step 1"
            assert report_data["steps"][0]["status"] == "success"

    finally:
        os.chdir(original_cwd) # Restore original working directory
