import pytest
import yaml
import os
import logging
import shutil
from embedded_ci_lab.loader import load_pipeline
from embedded_ci_lab.runner import execute_pipeline
from embedded_ci_lab.utils import setup_logging

@pytest.fixture(autouse=True)
def clean_log_dir_and_reset_logging(tmp_path):
    test_log_dir = tmp_path / "logs"
    test_log_file = test_log_dir / "test.log"

    logging.shutdown()
    os.makedirs(test_log_dir, exist_ok=True)
    setup_logging(str(test_log_file))

    yield str(test_log_file)

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
    
    yaml_steps = []
    for step in steps:
        s = {"name": step["name"], "command": step["command"]}
        if "timeout" in step:
            s["timeout_seconds"] = step["timeout"]
        if "retries" in step:
            s["retries"] = step["retries"]
        yaml_steps.append(s)
        
    content = {"name": name, "steps": yaml_steps}
    with open(p_file, 'w') as f:
        yaml.dump(content, f)
    return str(p_file)

def test_success_without_retry(tmp_path, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging
    pipeline_path = create_pipeline_file(tmp_path, "No Retry Success", [
        {"name": "Step 1", "command": "echo 'Hello'"}
    ])
    pipeline = load_pipeline(pipeline_path)
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path)
    assert "Step 1 ... (attempt 1/1)" not in log_content # No attempt info
    assert "Step 1 ... OK" in log_content

def test_failure_followed_by_success_on_retry(tmp_path, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging
    # A step that fails once and then succeeds.
    state_file = str(tmp_path / "state.txt").replace("\\", "/")
    # Use os.system to explicitly set exit code based on state file
    command = f'python -c "import os; ' \
              f's=\'{state_file}\'; ' \
              f'import sys; ' \
              f'exists = os.path.exists(s); ' \
              f'open(s, \'w\').write(\'done\'); ' \
              f'sys.exit(0 if exists else 1)"'
    
    pipeline_path = create_pipeline_file(tmp_path, "Retry Success", [
        {"name": "Retry Step", "command": command, "retries": 1}
    ])
    pipeline = load_pipeline(pipeline_path)
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path)
    assert "[1/1] Retry Step ... FAIL (attempt 1/2)" in log_content
    assert "[1/1] Retry Step ... OK (attempt 2/2)" in log_content

def test_failure_after_all_retries_exhausted(tmp_path, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging
    pipeline_path = create_pipeline_file(tmp_path, "Exhaust Retries", [
        {"name": "Step 1", "command": "exit 1", "retries": 2}
    ])
    pipeline = load_pipeline(pipeline_path)
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path)
    assert "[1/1] Step 1 ... FAIL (attempt 1/3)" in log_content
    assert "[1/1] Step 1 ... FAIL (attempt 2/3)" in log_content
    assert "[1/1] Step 1 ... FAIL (attempt 3/3)" in log_content
    assert "Pipeline 'Exhaust Retries' completed with status: failure." in log_content
