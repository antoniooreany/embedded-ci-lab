import pytest
import yaml
from embedded_ci_lab.loader import Pipeline, Step, load_pipeline, validate_pipeline, LoaderError

# --- Tests for load_pipeline (from previous step, ensuring changes didn't break it) ---
def test_load_valid_pipeline(tmp_path):
    p_file = tmp_path / "demo.yaml"
    content = {
        "name": "Test Pipeline",
        "steps": [
            {"name": "step1", "command": "echo 1"},
            {"name": "step2", "command": "echo 2", "params": {"key": "value"}}
        ]
    }
    p_file.write_text(yaml.dump(content))
    
    pipeline = load_pipeline(str(p_file))
    assert pipeline.name == "Test Pipeline"
    assert len(pipeline.steps) == 2
    assert pipeline.steps[0].name == "step1"
    assert pipeline.steps[0].command == "echo 1"
    assert pipeline.steps[1].params == {"key": "value"}

def test_load_missing_file():
    with pytest.raises(LoaderError, match="File not found"):
        load_pipeline("non_existent.yaml")

def test_load_invalid_yaml(tmp_path):
    p_file = tmp_path / "invalid.yaml"
    p_file.write_text("invalid: [yaml: structure")
    
    with pytest.raises(LoaderError, match="Failed to parse YAML"):
        load_pipeline(str(p_file))

def test_load_invalid_format_not_dict(tmp_path):
    p_file = tmp_path / "wrong.yaml"
    p_file.write_text("just a string")
    
    with pytest.raises(LoaderError, match="Invalid pipeline format"):
        load_pipeline(str(p_file))

def test_load_invalid_format_steps_not_list(tmp_path):
    p_file = tmp_path / "wrong_steps.yaml"
    content = {"name": "Pipe", "steps": "not_a_list"}
    p_file.write_text(yaml.dump(content))
    with pytest.raises(LoaderError, match="Invalid pipeline format: 'steps' must be a list"):
        load_pipeline(str(p_file))

def test_load_invalid_step_not_dict(tmp_path):
    p_file = tmp_path / "wrong_step.yaml"
    content = {"name": "Pipe", "steps": ["not_a_dict"]}
    p_file.write_text(yaml.dump(content))
    with pytest.raises(LoaderError, match="Invalid step at index 0: Expected a dictionary"):
        load_pipeline(str(p_file))

def test_load_missing_step_name_or_command(tmp_path):
    p_file = tmp_path / "missing_step_attr.yaml"
    content = {"name": "Pipe", "steps": [{"command": "cmd"}]}
    p_file.write_text(yaml.dump(content))
    with pytest.raises(LoaderError, match="Invalid step at index 0: 'name' must be a non-empty string"):
        load_pipeline(str(p_file))

    content = {"name": "Pipe", "steps": [{"name": "step"}]}
    p_file.write_text(yaml.dump(content))
    with pytest.raises(LoaderError, match="Invalid step at index 0: 'command' must be a non-empty string"):
        load_pipeline(str(p_file))

# --- New tests for validate_pipeline ---
def test_validate_valid_pipeline():
    pipeline = Pipeline(
        name="Valid Pipe",
        steps=[
            Step(name="Step 1", command="echo hello"),
            Step(name="Step 2", command="ls")
        ]
    )
    # Should not raise any error
    validate_pipeline(pipeline)

def test_validate_empty_pipeline_name():
    pipeline = Pipeline(
        name="",
        steps=[Step(name="Step 1", command="echo hello")]
    )
    with pytest.raises(LoaderError, match="'name' is required and cannot be empty"):
        validate_pipeline(pipeline)

def test_validate_pipeline_with_no_steps():
    pipeline = Pipeline(name="No Steps Pipe", steps=[])
    with pytest.raises(LoaderError, match="Pipeline must contain at least one step"):
        validate_pipeline(pipeline)

def test_validate_step_with_empty_name():
    pipeline = Pipeline(
        name="Pipe",
        steps=[Step(name="", command="echo hello")]
    )
    with pytest.raises(LoaderError, match="Step at index 0 requires a non-empty 'name'"):
        validate_pipeline(pipeline)

def test_validate_step_with_empty_command():
    pipeline = Pipeline(
        name="Pipe",
        steps=[Step(name="Step 1", command="")]
    )
    with pytest.raises(LoaderError, match="Step at index 0 requires a non-empty 'command'"):
        validate_pipeline(pipeline)

def test_validate_step_name_not_string(tmp_path):
    p_file = tmp_path / "invalid_step_name_type.yaml"
    content = {"name": "Pipe", "steps": [{"name": 123, "command": "cmd"}]}
    p_file.write_text(yaml.dump(content))
    with pytest.raises(LoaderError, match="Invalid step at index 0: 'name' must be a non-empty string"):
        load_pipeline(str(p_file))

def test_validate_step_command_not_string(tmp_path):
    p_file = tmp_path / "invalid_step_cmd_type.yaml"
    content = {"name": "Pipe", "steps": [{"name": "step", "command": 123}]}
    p_file.write_text(yaml.dump(content))
    with pytest.raises(LoaderError, match="Invalid step at index 0: 'command' must be a non-empty string"):
        load_pipeline(str(p_file))