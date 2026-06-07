import pytest
import os
import yaml
import subprocess
from embedded_ci_lab.models import Pipeline, Step
from embedded_ci_lab.loader import load_pipeline, validate_pipeline, LoaderError
from embedded_ci_lab.runner import execute_pipeline

# --- Tests from previous step (test_loader.py) are assumed to be in test_loader.py ---
# This file will focus on runner tests.

def create_pipeline_file(tmp_path, name, steps):
    p_file = tmp_path / f"{name.replace(' ', '_').lower()}.yaml"
    content = {"name": name, "steps": steps}
    p_file.write_text(yaml.dump(content))
    return str(p_file)

def test_successful_pipeline_execution(tmp_path, capsys):
    pipeline_path = create_pipeline_file(tmp_path, "Successful Pipe", [
        {"name": "Step A", "command": "echo 'Hello from A'"},
        {"name": "Step B", "command": "dir"}
    ])
    
    pipeline = load_pipeline(pipeline_path)
    result = execute_pipeline(pipeline)
    
    assert result.status == "success"
    captured = capsys.readouterr()
    assert "[1/2] Step A ... OK" in captured.out
    assert "[2/2] Step B ... OK" in captured.out
    assert "Pipeline 'Successful Pipe' completed with status: success." in captured.out

def test_failing_pipeline_stops_execution(tmp_path, capsys):
    pipeline_path = create_pipeline_file(tmp_path, "Failing Pipe", [
        {"name": "Step 1", "command": "echo 'First step'"},
        {"name": "Step 2", "command": "exit 1"}, # This step will fail
        {"name": "Step 3", "command": "echo 'Third step (should not run)'"}
    ])

    pipeline = load_pipeline(pipeline_path)
    result = execute_pipeline(pipeline)

    assert result.status == "failure"
    captured = capsys.readouterr()
    assert "[1/3] Step 1 ... OK" in captured.out
    assert "[2/3] Step 2 ... FAIL" in captured.out
    assert "Command 'exit 1' failed with exit code 1" in captured.err
    assert "Third step (should not run)" not in captured.out # Crucial check: must stop
    assert "Pipeline 'Failing Pipe' completed successfully." not in captured.out # Should not complete successfully
