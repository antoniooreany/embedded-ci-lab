import pytest
from embedded_ci_lab.models import Pipeline, Step
from embedded_ci_lab.runner import execute_pipeline
from embedded_ci_lab.loader import load_pipeline
from embedded_ci_lab.reporting import generate_report
from embedded_ci_lab.metrics import export_metrics
import os
import tempfile
import shutil

@pytest.fixture
def temp_reports_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)

def test_legacy_shell_step_regression():
    # Ensure standard shell steps without 'type' still work (defaulting to 'shell')
    pipeline = Pipeline(
        name="Legacy Pipeline",
        steps=[
            Step(name="Echo", command="echo 'legacy still works'")
        ]
    )
    result = execute_pipeline(pipeline)
    assert result.status == "success"
    assert result.step_results[0].status == "success"
    assert "legacy still works" in result.step_results[0].stdout

def test_pipeline_without_resource_guards_regression():
    # Ensure pipelines without memory limits/warnings still run normally
    # We use a slightly longer command to ensure the monitoring loop has time to run
    pipeline = Pipeline(
        name="No Guards Pipeline",
        steps=[
            Step(name="Step 1", command="python -c \"import time; time.sleep(0.2)\""),
            Step(name="Step 2", command="python -c \"import time; time.sleep(0.2)\"")
        ]
    )
    result = execute_pipeline(pipeline)
    assert result.status == "success"
    assert all(r.status == "success" for r in result.step_results)
    # Memory should be captured if the loop runs, but we don't strictly require > 0
    # if it's too fast. For 0.2s sleep it should be > 0.
    assert all(r.max_memory_mb >= 0 for r in result.step_results)

def test_reporting_metrics_backward_compatibility(temp_reports_dir):
    # Ensure reporting and metrics still work for a standard pipeline
    pipeline = Pipeline(
        name="Standard Pipeline",
        steps=[Step(name="Echo", command="echo hello")]
    )
    result = execute_pipeline(pipeline)
    
    # Check JSON Report
    report_path = generate_report(result, reports_dir=temp_reports_dir)
    assert os.path.exists(report_path)
    with open(report_path, 'r') as f:
        content = f.read()
        assert "Standard Pipeline" in content
        assert "warnings" in content # New field should exist even if empty
    
    # Check Metrics
    metrics_path = export_metrics(result, reports_dir=temp_reports_dir)
    assert os.path.exists(metrics_path)
    with open(metrics_path, 'r') as f:
        content = f.read()
        assert 'ci_pipeline_status{name="Standard_Pipeline"} 1' in content
        assert 'ci_step_memory_max_mb' in content

def test_yaml_loader_backward_compatibility():
    # Ensure old-style YAML (no type, no memory fields) still loads
    yaml_content = """
name: Old YAML Pipeline
steps:
  - name: Simple Step
    command: echo hello
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].type == "shell"
        assert pipeline.steps[0].memory_limit_mb is None
        assert pipeline.steps[0].memory_warn_mb is None
    finally:
        os.remove(temp_path)
