import pytest
import yaml
import os
import tempfile
from embedded_ci_lab.loader import load_pipeline, LoaderError

def test_load_yocto_validation_step():
    yaml_content = """
name: Yocto Validation Pipeline
steps:
  - name: Validate Artifacts
    type: yocto_validate_artifacts
    params:
      artifacts_dir: deploy/images/qemuarm
      expected:
        kernel: ["zImage"]
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.name == "Yocto Validation Pipeline"
        assert len(pipeline.steps) == 1
        step = pipeline.steps[0]
        assert step.name == "Validate Artifacts"
        assert step.type == "yocto_validate_artifacts"
        assert step.command is None
        assert step.params["artifacts_dir"] == "deploy/images/qemuarm"
    finally:
        os.remove(temp_path)

def test_load_shell_step_still_requires_command():
    yaml_content = """
name: Shell Pipeline
steps:
  - name: Run command
    type: shell
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        with pytest.raises(LoaderError, match="command' must be a non-empty string for shell steps"):
            load_pipeline(temp_path)
    finally:
        os.remove(temp_path)

def test_load_existing_pipeline_works():
    # Existing pipelines don't have 'type', should default to 'shell'
    yaml_content = """
name: Legacy Pipeline
steps:
  - name: Echo
    command: echo hello
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].type == "shell"
        assert pipeline.steps[0].command == "echo hello"
    finally:
        os.remove(temp_path)

def test_yocto_loader_demo_file_valid():
    # Smoke test for the official demo file
    pipeline = load_pipeline("pipelines/yocto_loader_demo.yaml")
    assert pipeline.name == "Yocto Loader Demo"
    assert pipeline.steps[1].type == "yocto_validate_artifacts"

def test_loader_fail_file_invalid():
    # Smoke test for the official failure case file
    with pytest.raises(LoaderError, match="command' must be a non-empty string for shell steps"):
        load_pipeline("pipelines/loader_fail_shell_missing_command.yaml")
