import pytest
import os
import tempfile
import yaml
from embedded_ci_lab.loader import load_pipeline

def test_env_var_substitution():
    # Set an env var
    os.environ["CI_WORKSPACE"] = "/home/user/workspace"
    
    yaml_content = """
name: Env Var Test
steps:
  - name: Test Step
    type: yocto_validate_artifacts
    params:
      artifacts_dir: "${CI_WORKSPACE}/build"
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = f.name
    
    try:
        pipeline = load_pipeline(temp_path)
        assert pipeline.steps[0].params["artifacts_dir"] == "/home/user/workspace/build"
    finally:
        os.remove(temp_path)
        del os.environ["CI_WORKSPACE"]
