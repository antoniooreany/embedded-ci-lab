import pytest
import time
import yaml
import os
import logging
import shutil
from embedded_ci_lab.loader import load_pipeline
from embedded_ci_lab.runner import execute_pipeline
from embedded_ci_lab.utils import setup_logging, LOG_FILE # Import setup_logging

@pytest.fixture(autouse=True)
def clean_log_dir_and_reset_logging(tmp_path):
    test_log_dir = tmp_path / "logs"
    test_log_file = test_log_dir / "test.log"

    # Before test:
    logging.shutdown()
    os.makedirs(test_log_dir, exist_ok=True)
    setup_logging(str(test_log_file))

    yield str(test_log_file)

    # After test:
    logging.shutdown()
    if os.path.exists(test_log_dir):
        shutil.rmtree(test_log_dir, ignore_errors=True)

def read_log_file(log_path):
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            return f.read()
    return ""

def create_pipeline_file(tmp_path, name, steps):
    p_file = tmp_path / f"{name.replace(' ', '_').lower()}.yaml"
    
    # Format steps properly for yaml.dump
    yaml_steps = []
    for step in steps:
        s = {"name": step["name"], "command": step["command"]}
        if "timeout" in step:
            s["timeout_seconds"] = step["timeout"]
        yaml_steps.append(s)
        
    content = {"name": name, "steps": yaml_steps}
    with open(p_file, 'w') as f:
        yaml.dump(content, f)
    return str(p_file)

def test_step_no_timeout_works(tmp_path, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging
    pipeline_path = create_pipeline_file(tmp_path, "No Timeout", [
        {"name": "Step 1", "command": "echo 'Hello'"}
    ])
    pipeline = load_pipeline(pipeline_path)
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path)
    assert "Step 1 ... OK" in log_content

def test_step_timeout_fails(tmp_path, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging
    pipeline_path = create_pipeline_file(tmp_path, "Timeout Fail", [
        {"name": "Slow Step", "command": 'python -c "import time; time.sleep(2)"', "timeout": 1}
    ])
    pipeline = load_pipeline(pipeline_path)
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path)
    assert "FAIL (Timeout after 1s)" in log_content

def test_pipeline_stops_after_timeout(tmp_path, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging
    pipeline_path = create_pipeline_file(tmp_path, "Stop After Timeout", [
        {"name": "Slow Step", "command": 'python -c "import time; time.sleep(2)"', "timeout": 1},
        {"name": "Next Step", "command": "echo 'Should not run'"}
    ])
    pipeline = load_pipeline(pipeline_path)
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path)
    assert "Slow Step ... FAIL" in log_content
    assert "Next Step" not in log_content
