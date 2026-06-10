import pytest
import os
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

def test_validate_artifacts_recursive(temp_artifacts_dir):
    # Setup nested structure
    os.makedirs(Path(temp_artifacts_dir, "conf"))
    os.makedirs(Path(temp_artifacts_dir, "meta-custom/conf"))
    
    Path(temp_artifacts_dir, "conf/local.conf").touch()
    Path(temp_artifacts_dir, "meta-custom/conf/layer.conf").touch()
    Path(temp_artifacts_dir, "bzImage").touch()
    
    patterns = {
        "kernel": ["bzImage"],
        "local_conf": ["conf/local.conf"],
        "layer_conf": ["meta-custom/conf/layer.conf"]
    }
    
    result = validate_artifacts(temp_artifacts_dir, patterns)
    
    assert result.validation_success is True
    assert result.found_artifacts["kernel"] == "bzImage"
    assert result.found_artifacts["local_conf"] == "conf/local.conf"
    assert result.found_artifacts["layer_conf"] == "meta-custom/conf/layer.conf"

def test_validate_artifacts_filename_match_in_subdir(temp_artifacts_dir):
    # Setup nested file
    os.makedirs(Path(temp_artifacts_dir, "nested/path"))
    Path(temp_artifacts_dir, "nested/path/artifact.txt").touch()
    
    # We look for the filename only
    patterns = {
        "nested_item": ["artifact.txt"]
    }
    
    result = validate_artifacts(temp_artifacts_dir, patterns)
    
    assert result.validation_success is True
    assert result.found_artifacts["nested_item"] == "nested/path/artifact.txt"
