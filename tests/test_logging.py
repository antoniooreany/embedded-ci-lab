import pytest
import os
import logging
import shutil
from embedded_ci_lab.loader import load_pipeline
from embedded_ci_lab.runner import execute_pipeline
from embedded_ci_lab.utils import setup_logging # Импорт setup_logging

@pytest.fixture(autouse=True)
def clean_log_dir_and_reset_logging(tmp_path): # Добавляем фикстуру tmp_path
    test_log_dir = tmp_path / "logs"
    test_log_file = test_log_dir / "test.log" # Отдельный лог-файл для каждого теста

    # Перед тестом:
    logging.shutdown() # Закрываем все предыдущие хендлеры логгера
    os.makedirs(test_log_dir, exist_ok=True)
    setup_logging(str(test_log_file)) # Конфигурируем логгер для текущего теста

    yield str(test_log_file) # Запускаем тест, возвращая путь к лог-файлу

    # После теста (teardown):
    logging.shutdown() # Закрываем все хендлеры, созданные для этого теста
    if os.path.exists(test_log_dir):
        shutil.rmtree(test_log_dir, ignore_errors=True) # Очищаем временную директорию

# Helper function to check log file content (адаптирована)
def read_log_file(log_path): # Принимает путь к лог-файлу
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            return f.read()
    return ""

def create_pipeline_file(tmp_path, name, steps):
    p_file = tmp_path / f"{name.replace(' ', '_').lower()}.yaml"
    with open(p_file, 'w') as f:
        f.write(f'name: "{name}"\nsteps:\n')
        for step in steps:
            f.write(f'  - name: "{step["name"]}"\n    command: "{step["command"]}"\n')
    return str(p_file)

def test_logging_successful_pipeline(tmp_path, caplog, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging # Get the path from the fixture

    pipeline_path = create_pipeline_file(tmp_path, "Logged Success", [
        {"name": "Log Step 1", "command": "echo 'Hello from log 1'"},
        {"name": "Log Step 2", "command": "echo 'Hello from log 2'"}
    ])
    pipeline = load_pipeline(pipeline_path)
    
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path) # Pass the path
    assert "Starting pipeline: Logged Success" in log_content
    assert "[1/2] Log Step 1 ... " in log_content # Check step start log
    assert "[1/2] Log Step 1 ... OK" in log_content # Check step result log
    assert "[2/2] Log Step 2 ... " in log_content
    assert "[2/2] Log Step 2 ... OK" in log_content
    assert "Pipeline 'Logged Success' completed with status: success." in log_content
    
    # Check stdout as well (using caplog.text for logging output)
    assert "Starting pipeline: Logged Success" in caplog.text
    assert "[1/2] Log Step 1 ... " in caplog.text # Only print "..." part as actual OK/FAIL is logged
    assert "[1/2] Log Step 1 ... OK" in caplog.text
    assert "Pipeline 'Logged Success' completed with status: success." in caplog.text


def test_logging_failing_pipeline(tmp_path, caplog, clean_log_dir_and_reset_logging):
    test_log_file_path = clean_log_dir_and_reset_logging # Get the path from the fixture

    pipeline_path = create_pipeline_file(tmp_path, "Logged Fail", [
        {"name": "Fail Step 1", "command": "echo 'Before fail'"},
        {"name": "Fail Step 2", "command": "exit 1"},
        {"name": "Fail Step 3", "command": "echo 'After fail'"}
    ])
    pipeline = load_pipeline(pipeline_path)
    
    execute_pipeline(pipeline)
    
    log_content = read_log_file(test_log_file_path) # Pass the path
    assert "Starting pipeline: Logged Fail" in log_content
    assert "[1/3] Fail Step 1 ... OK" in log_content
    assert "[2/3] Fail Step 2 ... FAIL" in log_content
    assert "Command 'exit 1' failed with exit code 1" in log_content
    assert "[3/3] Fail Step 3" not in log_content # Should not log non-executed step
    assert "Pipeline 'Logged Fail' completed with status: failure." in log_content

    # Check stdout as well (using caplog.text for logging output)
    assert "Starting pipeline: Logged Fail" in caplog.text
    assert "[2/3] Fail Step 2 ... FAIL" in caplog.text
    assert "Pipeline 'Logged Fail' completed with status: failure." in caplog.text
    assert "After fail" not in caplog.text