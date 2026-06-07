import os
from .models import PipelineResult

def export_metrics(pipeline_result: PipelineResult, reports_dir: str = "reports") -> str:
    """Exports pipeline results in Prometheus text format."""
    os.makedirs(reports_dir, exist_ok=True)
    filename = os.path.join(reports_dir, "latest_metrics.prom")

    lines = []
    
    # Global pipeline metrics
    pipeline_name = pipeline_result.pipeline_name.replace(" ", "_")
    status_val = 1 if pipeline_result.status == "success" else 0
    duration = (pipeline_result.finished_at - pipeline_result.started_at).total_seconds()
    
    lines.append(f'ci_pipeline_status{{name="{pipeline_name}"}} {status_val}')
    lines.append(f'ci_pipeline_duration_seconds{{name="{pipeline_name}"}} {duration:.3f}')
    
    # Per-step metrics
    for step_res in pipeline_result.step_results:
        step_name = step_res.name.replace(" ", "_")
        
        lines.append(f'ci_step_duration_seconds{{pipeline="{pipeline_name}", step="{step_name}"}} {step_res.duration_seconds:.3f}')
        lines.append(f'ci_step_memory_max_mb{{pipeline="{pipeline_name}", step="{step_name}"}} {step_res.max_memory_mb:.2f}')
        lines.append(f'ci_step_retries_total{{pipeline="{pipeline_name}", step="{step_name}"}} {step_res.retry_count}')
        
        timeout_val = 1 if step_res.exit_code == 124 else 0
        lines.append(f'ci_step_timeout_total{{pipeline="{pipeline_name}", step="{step_name}"}} {timeout_val}')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")
        
    return filename
