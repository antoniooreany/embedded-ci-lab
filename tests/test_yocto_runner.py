import pytest
import shutil
import tempfile
from pathlib import Path
from embedded_ci_lab.models import Pipeline, Step
from embedded_ci_lab.runner import execute_pipeline

@pytest.fixture
def temp_artifacts_root():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)

def test_run_yocto_validation_success(temp_artifacts_root, caplog):
    # Setup success case
    Path(temp_artifacts_root, "zImage").touch()
    Path(temp_artifacts_root, "rootfs.ext4").touch()
    
    pipeline = Pipeline(
        name="Test Pipeline",
        steps=[
            Step(
                name="Check Artifacts",
                type="yocto_validate_artifacts",
                params={
                    "artifacts_root": temp_artifacts_root,
                    "expected": {
                        "kernel": ["zImage"],
                        "rootfs": ["*.ext4"]
                    }
                }
            )
        ]
    )
    
    result = execute_pipeline(pipeline)
    
    assert result.status == "success"
    assert len(result.step_results) == 1
    step_res = result.step_results[0]
    assert step_res.status == "success"
    assert "kernel" in step_res.stdout
    assert "Found artifacts: ['kernel', 'rootfs']" in caplog.text

def test_run_yocto_validation_failure_stops_pipeline(temp_artifacts_root, caplog):
    # Setup failure case (missing artifacts)
    pipeline = Pipeline(
        name="Fail Pipeline",
        steps=[
            Step(
                name="Check Missing",
                type="yocto_validate_artifacts",
                params={
                    "artifacts_root": temp_artifacts_root,
                    "expected": {"kernel": ["zImage"]}
                }
            ),
            Step(name="Should not run", command="echo unreachable")
        ]
    )
    
    result = execute_pipeline(pipeline)
    
    assert result.status == "failure"
    assert len(result.step_results) == 1 # Second step should not have run
    assert result.step_results[0].status == "failure"
    assert "Missing artifacts: ['kernel']" in caplog.text
    assert "Should not run" not in caplog.text

def test_run_yocto_validation_with_retries(temp_artifacts_root):
    # Validation usually doesn't need retries, but we check it works technically
    # First attempt fails, then we create file, second attempt should pass if we could change env mid-run
    # But here we just check that retries are attempted if fail
    
    pipeline = Pipeline(
        name="Retry Pipeline",
        steps=[
            Step(
                name="Check With Retry",
                type="yocto_validate_artifacts",
                retries=1,
                params={
                    "artifacts_root": temp_artifacts_root,
                    "expected": {"kernel": ["zImage"]}
                }
            )
        ]
    )
    
    # It will fail twice
    result = execute_pipeline(pipeline)
    assert result.step_results[0].retry_count == 1
    assert result.status == "failure"
