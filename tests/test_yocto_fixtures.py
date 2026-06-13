import os
from embedded_ci_lab.loader import load_pipeline
from embedded_ci_lab.runner import execute_pipeline

def test_yocto_validate_demo_pipeline_execution():
    # Verify the successful demo pipeline actually passes
    pipeline = load_pipeline("pipelines/integration/yocto_validate_demo.yaml")
    result = execute_pipeline(pipeline)
    
    assert result.status == "success"
    assert result.step_results[0].name == "Validate Successful Build"
    assert result.step_results[0].status == "success"

def test_yocto_validate_fail_demo_pipeline_execution():
    # Verify the failure demo pipeline actually fails
    pipeline = load_pipeline("pipelines/integration/yocto_validate_fail_demo.yaml")
    result = execute_pipeline(pipeline)
    
    assert result.status == "failure"
    assert result.step_results[0].name == "Expect Validation Failure"
    assert result.step_results[0].status == "failure"
    assert "rootfs" in result.step_results[0].stdout
    assert "manifest" in result.step_results[0].stdout

def test_fixture_directories_exist():
    assert os.path.isdir("tests/fixtures/yocto_artifacts/success")
    assert os.path.isdir("tests/fixtures/yocto_artifacts/fail")
    assert os.path.isfile("tests/fixtures/yocto_artifacts/success/bzImage")
