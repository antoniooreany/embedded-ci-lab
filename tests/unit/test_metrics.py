import os
from datetime import datetime
from embedded_ci_lab.models import PipelineResult, StepResult
from embedded_ci_lab.metrics import export_metrics

def create_dummy_pipeline_result(status="success") -> PipelineResult:
    now = datetime.now()
    return PipelineResult(
        pipeline_name="Test Pipeline",
        started_at=now,
        finished_at=now,
        status=status,
        step_results=[
            StepResult(
                name="Step 1",
                command="echo 1",
                status="success",
                exit_code=0,
                started_at=now,
                finished_at=now,
                duration_seconds=1.23,
                stdout="out",
                stderr="",
                max_memory_mb=10.0,
                retry_count=0
            )
        ]
    )

def test_metrics_export_creates_file(tmp_path):
    reports_dir = tmp_path / "reports"
    pipeline_result = create_dummy_pipeline_result()
    metrics_file = export_metrics(pipeline_result, str(reports_dir))

    assert os.path.exists(metrics_file)
    assert "latest_metrics.prom" in metrics_file

def test_metrics_export_content(tmp_path):
    reports_dir = tmp_path / "reports"
    pipeline_result = create_dummy_pipeline_result(status="failure")
    metrics_file = export_metrics(pipeline_result, str(reports_dir))

    with open(metrics_file, 'r') as f:
        content = f.read()
    
    assert 'ci_pipeline_status{name="Test_Pipeline"} 0' in content
    assert 'ci_step_duration_seconds{pipeline="Test_Pipeline", step="Step_1"} 1.230' in content
    assert 'ci_step_memory_max_mb{pipeline="Test_Pipeline", step="Step_1"} 10.00' in content
    assert 'ci_step_retries_total{pipeline="Test_Pipeline", step="Step_1"} 0' in content
