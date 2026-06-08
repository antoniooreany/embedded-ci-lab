import pytest
from embedded_ci_lab.models import Pipeline, Step
from embedded_ci_lab.runner import execute_pipeline
from embedded_ci_lab.loader import load_pipeline, LoaderError
import tempfile
import os

def test_memory_limit_success():
    # Small allocation should pass
    pipeline = Pipeline(
        name="Memory Success",
        steps=[
            Step(
                name="Low Memory",
                command="python -c \"import time; x = ' ' * 1024 * 1024; time.sleep(0.5)\"", # ~1MB
                memory_limit_mb=100.0
            )
        ]
    )
    result = execute_pipeline(pipeline)
    assert result.status == "success"
    assert result.step_results[0].status == "success"
    assert result.step_results[0].max_memory_mb > 0

def test_memory_limit_failure():
    # Large allocation should fail
    pipeline = Pipeline(
        name="Memory Failure",
        steps=[
            Step(
                name="High Memory",
                command="python -c \"import time; x = ' ' * 50 * 1024 * 1024; time.sleep(1)\"", # ~50MB
                memory_limit_mb=10.0
            )
        ]
    )
    result = execute_pipeline(pipeline)
    assert result.status == "failure"
    assert result.step_results[0].status == "failure"
    assert "Memory limit exceeded" in result.step_results[0].stderr

def test_memory_warning_success():
    # Allocation above warning but below limit
    pipeline = Pipeline(
        name="Memory Warning",
        steps=[
            Step(
                name="Warning Step",
                command="python -c \"import time; x = ' ' * 20 * 1024 * 1024; time.sleep(0.5)\"", # ~20MB
                memory_limit_mb=100.0,
                memory_warn_mb=10.0
            )
        ]
    )
    result = execute_pipeline(pipeline)
    assert result.status == "success"
    assert result.step_results[0].status == "success"
    assert len(result.step_results[0].warnings) > 0
    assert any("Memory usage warning" in w for w in result.step_results[0].warnings)

def test_no_memory_warning_if_below_threshold():
    pipeline = Pipeline(
        name="No Warning",
        steps=[
            Step(
                name="Quiet Step",
                command="python -c \"import time; x = ' ' * 1 * 1024 * 1024; time.sleep(0.5)\"", # ~1MB
                memory_limit_mb=100.0,
                memory_warn_mb=50.0
            )
        ]
    )
    result = execute_pipeline(pipeline)
    assert result.status == "success"
    assert len(result.step_results[0].warnings) == 0

def test_loader_memory_warning():
    yaml_content = """
name: Memory Warn Pipeline
steps:
  - name: Warn Step
    command: echo hello
    memory_warn_mb: 25.0
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].memory_warn_mb == 25.0
    finally:
        os.remove(temp_path)

def test_loader_memory_limit():
    yaml_content = """
name: Memory Limit Pipeline
steps:
  - name: Limited Step
    command: echo hello
    memory_limit_mb: 50.5
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].memory_limit_mb == 50.5
    finally:
        os.remove(temp_path)

def test_loader_invalid_memory_limit():
    yaml_content = """
name: Invalid Memory
steps:
  - name: Bad Limit
    command: echo hello
    memory_limit_mb: "not a number"
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        with pytest.raises(LoaderError, match="memory_limit_mb' must be a number"):
            load_pipeline(temp_path)
    finally:
        os.remove(temp_path)
