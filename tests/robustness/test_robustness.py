import os
import pytest
import threading
from datetime import datetime
from hypothesis import given, strategies as st
from embedded_ci_lab.loader import expand_env_vars
from embedded_ci_lab.reporting import generate_report
from embedded_ci_lab.models import PipelineResult

# --- Property-Based Testing for expand_env_vars ---

@given(st.text())
def test_expand_env_vars_never_crashes(text):
    """
    Property: expand_env_vars should never crash, regardless of the input string.
    This demonstrates robustness against malformed or malicious environment variable syntax.
    """
    try:
        expand_env_vars(text)
    except Exception as e:
        pytest.fail(f"expand_env_vars crashed with input {text!r}: {e}")

@given(st.text(alphabet=st.characters(blacklist_categories=('Cs',), blacklist_characters=('$', '{', '}', ':', '-'))))
def test_expand_env_vars_preserves_plain_text(text):
    """
    Property: plain text without special characters should remain unchanged.
    """
    assert expand_env_vars(text) == text

@given(st.text(min_size=1, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters=('_'))))
def test_expand_env_vars_bash_default_logic(var_name):
    """
    Property: ${VAR:-default} should return 'default' if VAR is not in environment.
    """
    # Ensure the variable is NOT in the environment
    if var_name in os.environ:
        del os.environ[var_name]
    
    input_str = f"${{{var_name}:-fallback_value}}"
    assert expand_env_vars(input_str) == "fallback_value"

# --- Concurrency Tests for Reporting ---

def test_concurrent_report_generation(tmp_path):
    """
    Test: Simulating multiple pipelines finishing at the exact same microsecond (mocked).
    Verify: No file collisions or race conditions during report generation.
    """
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    
    # We mock a fixed start time to force identical timestamps if we were using just seconds.
    # However, generate_report uses strftime("%Y%m%d%H%M%S"), so even if we run 
    # threads at the same time, they might hit the same second.
    fixed_time = datetime(2026, 6, 12, 20, 0, 0)
    
    def create_mock_result(name):
        return PipelineResult(
            pipeline_name=name,
            started_at=fixed_time,
            finished_at=fixed_time,
            status="success",
            step_results=[]
        )

    results = [create_mock_result(f"Pipeline {i}") for i in range(10)]
    report_paths = []
    errors = []

    def task(result):
        try:
            path = generate_report(result, reports_dir=str(reports_dir))
            report_paths.append(path)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=task, args=(res,)) for res in results]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Errors occurred during concurrent reporting: {errors}"
    
    # Check that we have 10 distinct files
    # Because names are different ("Pipeline 0", "Pipeline 1"), 
    # the sanitized filenames will be different even if the timestamp is identical.
    unique_reports = set(report_paths)
    assert len(unique_reports) == 10
    assert len(list(reports_dir.glob("*.json"))) == 10

def test_identical_pipeline_names_collision_risk(tmp_path):
    """
    Test: If two identical pipelines start at the exact same second, we want to know
    how the system behaves. Currently, generate_report uses timestamp + name.
    If they are identical, they will overwrite each other.
    This test documents this current behavior (or we could fix it if it's a bug).
    """
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    fixed_time = datetime(2026, 6, 12, 20, 0, 0)
    
    res1 = PipelineResult("Same", fixed_time, fixed_time, "success", [])
    res2 = PipelineResult("Same", fixed_time, fixed_time, "success", [])
    
    path1 = generate_report(res1, reports_dir=str(reports_dir))
    path2 = generate_report(res2, reports_dir=str(reports_dir))
    
    # Current implementation: same filename
    assert path1 == path2
    # In a real high-load CI, we might want to add a UUID or microsecond to the filename.
    # For now, we document that the last one wins.
