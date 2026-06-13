import pytest
import os
import tempfile
from embedded_ci_lab.loader import load_pipeline

def test_env_var_substitution_with_default():
    # Ensure no environment variable exists
    if "UNDEFINED_VAR" in os.environ:
        del os.environ["UNDEFINED_VAR"]
    
    yaml_content = """
name: Env Var Default Test
steps:
  - name: Test Step
    type: yocto_validate_artifacts
    params:
      artifacts_root: "${UNDEFINED_VAR:-/tmp/default}"
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].params["artifacts_root"] == "/tmp/default"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_env_var_substitution_existing():
    # Set an env var
    os.environ["EXISTING_VAR"] = "/home/user/custom"
    
    yaml_content = """
name: Env Var Existing Test
steps:
  - name: Test Step
    type: yocto_validate_artifacts
    params:
      artifacts_root: "${EXISTING_VAR:-/tmp/default}"
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].params["artifacts_root"] == "/home/user/custom"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        del os.environ["EXISTING_VAR"]

def test_standard_env_var_substitution():
    os.environ["CI_BUILD_ID"] = "12345"
    yaml_content = """
name: Standard Env Var Test
steps:
  - name: Echo Build ID
    command: echo "Building ID-${CI_BUILD_ID}"
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].command == "echo \"Building ID-12345\""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        del os.environ["CI_BUILD_ID"]
