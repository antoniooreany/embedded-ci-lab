import pytest
import shutil
import tempfile
from pathlib import Path
from embedded_ci_lab.yocto_validator import validate_artifacts

@pytest.fixture
def temp_artifacts_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)

def test_validate_artifacts_success(temp_artifacts_dir):
    # Setup files
    Path(temp_artifacts_dir, "zImage").touch()
    Path(temp_artifacts_dir, "core-image-minimal.wic.gz").touch()
    Path(temp_artifacts_dir, "core-image-minimal.manifest").touch()
    
    patterns = {
        "kernel": ["zImage", "Image", "bzImage"],
        "rootfs": ["*.wic", "*.wic.gz", "*.ext4"],
        "manifest": ["*.manifest"]
    }
    
    result = validate_artifacts(temp_artifacts_dir, patterns)
    
    assert result.validation_success is True
    assert "kernel" in result.found_artifacts
    assert result.found_artifacts["kernel"] == "zImage"
    assert "rootfs" in result.found_artifacts
    assert "manifest" in result.found_artifacts
    assert not result.missing_artifacts

def test_validate_artifacts_missing_some(temp_artifacts_dir):
    # Only kernel exists
    Path(temp_artifacts_dir, "zImage").touch()
    
    patterns = {
        "kernel": ["zImage"],
        "rootfs": ["*.wic"]
    }
    
    result = validate_artifacts(temp_artifacts_dir, patterns)
    
    assert result.validation_success is False
    assert "kernel" in result.found_artifacts
    assert "rootfs" in result.missing_artifacts

def test_validate_artifacts_multiple_acceptable_names(temp_artifacts_dir):
    # Both Image and zImage exist, should match 'kernel'
    Path(temp_artifacts_dir, "Image").touch()
    
    patterns = {
        "kernel": ["zImage", "Image"]
    }
    
    result = validate_artifacts(temp_artifacts_dir, patterns)
    
    assert result.validation_success is True
    assert result.found_artifacts["kernel"] == "Image"

def test_validate_artifacts_empty_directory(temp_artifacts_dir):
    patterns = {
        "kernel": ["zImage"]
    }
    
    result = validate_artifacts(temp_artifacts_dir, patterns)
    
    assert result.validation_success is False
    assert "kernel" in result.missing_artifacts

def test_validate_artifacts_non_existent_directory():
    result = validate_artifacts("non_existent_dir_12345", {"any": ["*"]})
    assert result.validation_success is False
    assert any("not exist" in w for w in result.warnings)
