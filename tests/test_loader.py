import pytest
import os
import yaml
from embedded_ci_lab.loader import load_pipeline, LoaderError

def test_load_valid_pipeline(tmp_path):
    p_file = tmp_path / "demo.yaml"
    content = {
        "name": "Test Pipeline",
        "steps": [
            {"name": "step1", "command": "echo 1"},
            {"name": "step2", "command": "echo 2"}
        ]
    }
    p_file.write_text(yaml.dump(content))
    
    pipeline = load_pipeline(str(p_file))
    assert pipeline.name == "Test Pipeline"
    assert len(pipeline.steps) == 2
    assert pipeline.steps[0].name == "step1"

def test_load_missing_file():
    with pytest.raises(LoaderError, match="File not found"):
        load_pipeline("non_existent.yaml")

def test_load_invalid_yaml(tmp_path):
    p_file = tmp_path / "invalid.yaml"
    p_file.write_text("invalid: [yaml: structure")
    
    with pytest.raises(LoaderError, match="Failed to parse YAML"):
        load_pipeline(str(p_file))

def test_load_invalid_format(tmp_path):
    p_file = tmp_path / "wrong.yaml"
    p_file.write_text("just a string")
    
    with pytest.raises(LoaderError, match="Invalid pipeline format"):
        load_pipeline(str(p_file))
