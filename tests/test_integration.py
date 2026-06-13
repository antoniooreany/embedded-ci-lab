import pytest
import os
import shutil
import json
from pathlib import Path
from embedded_ci_lab.cli import main
from unittest.mock import patch

@pytest.fixture
def mock_yocto_lab(tmp_path):
    # Create yocto-lab directory structure as expected by pipelines
    yocto_lab = tmp_path / "yocto-lab"
    yocto_lab.mkdir()
    
    # Required metadata structure
    for subdir in ["samples", "conf-examples", "templates"]:
        (yocto_lab / subdir).mkdir()
        (yocto_lab / subdir / "local.conf").touch()
        (yocto_lab / subdir / "bblayers.conf").touch()
    
    (yocto_lab / "meta-custom" / "conf").mkdir(parents=True)
    (yocto_lab / "meta-custom" / "conf" / "layer.conf").touch()
    
    (yocto_lab / "sample_recipe_1.0.bb").touch()
    
    return yocto_lab

def test_yocto_policy_gate_fail_scenario(mock_yocto_lab, monkeypatch, capsys):
    # Path to existing pipeline
    pipeline_path = str(Path(__file__).parent.parent / "pipelines" / "integration" / "yocto_policy_gate_fail.yaml")
    
    # meta-security is MISSING by default in mock_yocto_lab -> triggers failure
    monkeypatch.setenv("ARTIFACTS_ROOT", str(mock_yocto_lab))
    
    # Run from a temporary directory to avoid polluting the repo with reports/logs
    temp_work_dir = mock_yocto_lab.parent / "ci_work"
    temp_work_dir.mkdir()
    os.makedirs(temp_work_dir / "reports", exist_ok=True)
    os.makedirs(temp_work_dir / "logs", exist_ok=True)
    monkeypatch.chdir(temp_work_dir)
    
    with patch("sys.argv", ["embedded-ci", "run", "--pipeline", pipeline_path]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        
        assert excinfo.value.code == 1
    
    captured = capsys.readouterr()
    # The yocto_validator output should mention missing mandatory_security_layer
    # In runner.py: logger.error(f"Missing artifacts: {result.missing_artifacts}")
    assert "mandatory_security_layer" in captured.out or "mandatory_security_layer" in captured.err
    assert "FAIL" in captured.out or "failure" in captured.out.lower()

def test_yocto_full_cycle_success_scenario(mock_yocto_lab, monkeypatch, capsys):
    pipeline_path = str(Path(__file__).parent.parent / "pipelines" / "integration" / "yocto_full_cycle_success.yaml")
    
    # This pipeline uses '../yocto-lab' in shell commands.
    # So we must be in a directory that is a sibling to yocto-lab.
    temp_work_dir = mock_yocto_lab.parent / "work"
    temp_work_dir.mkdir()
    os.makedirs(temp_work_dir / "reports", exist_ok=True)
    os.makedirs(temp_work_dir / "logs", exist_ok=True)
    
    monkeypatch.setenv("ARTIFACTS_ROOT", str(mock_yocto_lab))
    monkeypatch.chdir(temp_work_dir)
    
    with patch("sys.argv", ["embedded-ci", "run", "--pipeline", pipeline_path]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        
        assert excinfo.value.code == 0
    
    captured = capsys.readouterr()
    # Check for memory warning (80MB > 50MB warn threshold)
    assert "Memory usage warning" in captured.out or "Memory usage warning" in captured.err
    
    # Verify the JSON report for detailed command output
    report_files = list(Path(temp_work_dir / "reports").glob("*.json"))
    # Skip 'latest.json' if it exists, or just find the one that isn't it
    real_reports = [f for f in report_files if f.name != "latest.json"]
    assert len(real_reports) > 0
    report_file = real_reports[0]
    
    with open(report_file, "r") as f:
        report_data = json.load(f)
    
    assert report_data["status"] == "success"
    
    # Check that 'Build artifacts generated successfully' is in the stdout of the build step
    build_step = next(s for s in report_data["steps"] if "[Build]" in s["name"])
    assert "Build artifacts generated successfully" in build_step["stdout"]
    
    # Verify warning is also in the report
    assert any("Memory usage warning" in w for w in build_step["warnings"])

