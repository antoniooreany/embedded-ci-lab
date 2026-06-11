import os
import yaml
import re
from typing import Any
from .models import Pipeline, Step

class LoaderError(Exception):
    """Custom exception for pipeline loading errors."""
    pass

def expand_env_vars(data: Any) -> Any:
    """
    Recursively expand environment variables in configuration data.
    Supports standard ${VAR} and Bash-style default values ${VAR:-default}.
    """
    if isinstance(data, dict):
        return {k: expand_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [expand_env_vars(v) for v in data]
    elif isinstance(data, str):
        # Handle ${VAR:-default} syntax
        def replace_with_default(match):
            var_name = match.group(1)
            default_val = match.group(2)
            return os.environ.get(var_name, default_val)
        
        # Regex to find ${VAR:-default}
        data = re.sub(r'\$\{([^}:]+):-(.*?)\}', replace_with_default, data)
        # Handle standard environment variables ($VAR, ${VAR})
        return os.path.expandvars(data)
    return data

def load_pipeline(file_path: str) -> Pipeline:
    if not os.path.exists(file_path):
        raise LoaderError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise LoaderError(f"Failed to parse YAML: {e}")
    
    # Expand environment variables
    data = expand_env_vars(data)
    
    if not data or not isinstance(data, dict):
        raise LoaderError("Invalid pipeline format: Expected a dictionary at root")
    
    raw_name = data.get("name")
    if not isinstance(raw_name, str):
        raise LoaderError("Invalid pipeline format: 'name' must be a string")
    name = raw_name
    
    steps_data = data.get("steps", [])
    
    if not isinstance(steps_data, list):
        raise LoaderError("Invalid pipeline format: 'steps' must be a list")
    
    steps = []
    for i, s in enumerate(steps_data):
        if not isinstance(s, dict):
            raise LoaderError(f"Invalid step at index {i}: Expected a dictionary")
        
        step_name = s.get("name")
        step_type = s.get("type", "shell")
        step_command = s.get("command")

        if not isinstance(step_name, str) or not step_name:
            raise LoaderError(f"Invalid step at index {i}: 'name' must be a non-empty string")
        
        if step_type == "shell":
            if not isinstance(step_command, str) or not step_command:
                raise LoaderError(f"Invalid step at index {i}: 'command' must be a non-empty string for shell steps")
        
        timeout_seconds = s.get("timeout_seconds")
        if timeout_seconds is not None and not isinstance(timeout_seconds, int):
             raise LoaderError(f"Invalid step at index {i}: 'timeout_seconds' must be an integer")
        
        retries = s.get("retries", 0)
        if not isinstance(retries, int) or retries < 0:
             raise LoaderError(f"Invalid step at index {i}: 'retries' must be a non-negative integer")
        
        memory_limit_mb = s.get("memory_limit_mb")
        if memory_limit_mb is not None and not isinstance(memory_limit_mb, (int, float)):
             raise LoaderError(f"Invalid step at index {i}: 'memory_limit_mb' must be a number")

        memory_warn_mb = s.get("memory_warn_mb")
        if memory_warn_mb is not None and not isinstance(memory_warn_mb, (int, float)):
             raise LoaderError(f"Invalid step at index {i}: 'memory_warn_mb' must be a number")
            
        steps.append(Step(
            name=step_name, 
            command=step_command,
            type=step_type,
            params=s.get("params", {}),
            timeout_seconds=timeout_seconds,
            memory_limit_mb=memory_limit_mb,
            memory_warn_mb=memory_warn_mb,
            retries=retries
        ))
        
    return Pipeline(name=name, steps=steps)

def validate_pipeline(pipeline: Pipeline) -> None:
    if not isinstance(pipeline.name, str) or not pipeline.name.strip():
        raise LoaderError("Pipeline validation error: 'name' is required and cannot be empty.")
    if not pipeline.steps:
        raise LoaderError("Pipeline validation error: Pipeline must contain at least one step.")
    
    for i, step in enumerate(pipeline.steps):
        if not isinstance(step.name, str) or not step.name.strip():
            raise LoaderError(f"Pipeline validation error: Step at index {i} requires a non-empty 'name'.")
        
        if step.type == "shell":
            if not isinstance(step.command, str) or not step.command.strip():
                raise LoaderError(f"Pipeline validation error: Step at index {i} requires a non-empty 'command' for shell steps.")
