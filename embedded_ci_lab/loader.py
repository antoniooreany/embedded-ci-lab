import yaml
import os
from .models import Pipeline, Step

class LoaderError(Exception):
    """Custom exception for pipeline loading errors."""
    pass

def load_pipeline(file_path: str) -> Pipeline:
    if not os.path.exists(file_path):
        raise LoaderError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise LoaderError(f"Failed to parse YAML: {e}")
    
    if not data or not isinstance(data, dict):
        raise LoaderError("Invalid pipeline format: Expected a dictionary at root")
    
    name = data.get("name", "Unnamed Pipeline")
    steps_data = data.get("steps", [])
    
    if not isinstance(steps_data, list):
        raise LoaderError("Invalid pipeline format: 'steps' must be a list")
    
    steps = []
    for i, s in enumerate(steps_data):
        if not isinstance(s, dict) or "name" not in s or "command" not in s:
            raise LoaderError(f"Invalid step at index {i}: 'name' and 'command' are required")
        steps.append(Step(name=s["name"], command=s["command"]))
        
    return Pipeline(name=name, steps=steps)
