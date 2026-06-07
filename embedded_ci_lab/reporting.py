import json
import os
import re
from datetime import datetime
from typing import Dict, Any
from .models import PipelineResult

def sanitize_filename(name: str) -> str:
    """Sanitizes a string to be used as a filename."""
    # Replace non-alphanumeric characters (excluding underscores) with underscores
    name = re.sub(r'[^a-zA-Z0-9_]', "_", name)
    # Replace multiple underscores with a single underscore
    name = re.sub(r'_+', "_", name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Convert to lowercase
    name = name.lower()
    return name

def generate_report(pipeline_result: PipelineResult, reports_dir: str = "reports") -> str:
    """Generates a JSON report file for a pipeline execution."""
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = pipeline_result.started_at.strftime("%Y%m%d%H%M%S")
    sanitized_name = sanitize_filename(pipeline_result.pipeline_name)
    filename = os.path.join(reports_dir, f"{timestamp}_{sanitized_name}.json")

    steps_data: list[Dict[str, Any]] = []

    for step_res in pipeline_result.step_results:
        steps_data.append({
            "name": step_res.name,
            "command": step_res.command,
            "status": step_res.status,
            "exit_code": step_res.exit_code,
            "started_at": step_res.started_at.isoformat(),
            "finished_at": step_res.finished_at.isoformat(),
            "duration_seconds": step_res.duration_seconds,
            "max_memory_mb": step_res.max_memory_mb,
            "retry_count": step_res.retry_count,
            "stdout": step_res.stdout,
            "stderr": step_res.stderr,
        })

    report_data: Dict[str, Any] = {
        "pipeline_name": pipeline_result.pipeline_name,
        "started_at": pipeline_result.started_at.isoformat(),
        "finished_at": pipeline_result.finished_at.isoformat(),
        "status": pipeline_result.status,
        "steps": steps_data,
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)
        
    return filename
