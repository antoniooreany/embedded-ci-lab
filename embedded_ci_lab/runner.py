from embedded_ci_lab.models import Step


import subprocess
import logging
import psutil
import time
import json
from datetime import datetime
from .models import Pipeline, PipelineResult, StepResult
from .yocto_validator import validate_artifacts

logger = logging.getLogger(__name__)

def execute_pipeline(pipeline: Pipeline) -> PipelineResult:
    """
    Executes all steps in a pipeline sequentially.

    Supports shell commands and specialized step types like Yocto artifact validation.
    Implements retries, timeouts, and resource guarding (memory limits/warnings).
    Stops execution on the first unrecoverable failure (fail-fast).
    """
    pipeline_started_at = datetime.now()
    step_results = []
    pipeline_overall_status = "success"

    logger.info(f"Starting pipeline: {pipeline.name}")
    
    total_steps = len(pipeline.steps)
    for i, step in enumerate[Step](pipeline.steps):
        step_number = i + 1
        log_prefix = f"[{step_number}/{total_steps}]"
        
        attempt = 0
        max_attempts = step.retries + 1
        success = False
        
        step_started_at = datetime.now()
        
        while attempt < max_attempts:
            attempt += 1
            attempt_prefix = f" (attempt {attempt}/{max_attempts})" if step.retries > 0 else ""
            
            logger.info(f"{log_prefix} {step.name} ... {attempt_prefix}")
            
            step_status = "failure" 
            exit_code = -1
            stdout_output = ""
            stderr_output = ""
            max_memory_mb = 0.0
            step_warnings = []

            try:
                if step.type == "yocto_validate_artifacts":
                    artifacts_root = step.params.get("artifacts_root", ".")
                    expected = step.params.get("expected", {})

                    result = validate_artifacts(artifacts_root, expected)

                    
                    # Prepare detail string for reports/logs
                    details = {
                        "found": result.found_artifacts,
                        "missing": result.missing_artifacts,
                        "warnings": result.warnings
                    }
                    stdout_output = json.dumps(details, indent=2)
                    
                    if result.validation_success:
                        logger.info(f"{log_prefix} {step.name} ... OK{attempt_prefix}")
                        logger.info(f"Found artifacts: {list[str](result.found_artifacts.keys())}")
                        step_status = "success"
                        exit_code = 0
                        success = True
                    else:
                        logger.error(f"{log_prefix} {step.name} ... FAIL{attempt_prefix}")
                        if result.missing_artifacts:
                            logger.error(f"Missing artifacts: {result.missing_artifacts}")
                        if result.warnings:
                            logger.error(f"Validation warnings: {result.warnings}")
                        step_status = "failure"
                        exit_code = 1
                    
                    # Validation is internal, memory usage is negligible but we can record it
                    max_memory_mb = psutil.Process().memory_info().rss / (1024 * 1024)
                    
                    if success:
                        break # Success, move to next step
                
                else: # Default shell type
                    # Use timeout if specified
                    timeout = step.timeout_seconds if step.timeout_seconds else None
                    cmd = step.command if step.command else ""
                    
                    # Start process and monitor
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    ps_process = psutil.Process(process.pid)
                    
                    # Monitor memory and timeout
                    start_time = time.time()
                    while process.poll() is None:
                        # Check timeout
                        if timeout and (time.time() - start_time) > timeout:
                            process.kill()
                            raise subprocess.TimeoutExpired(cmd, timeout)
                            
                        try:
                            # Find all child processes recursively
                            all_procs = ps_process.children(recursive=True) + [ps_process]
                            current_mem_mb = 0.0
                            for p in all_procs:
                                try:
                                    current_mem_mb += p.memory_info().rss / (1024 * 1024)
                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                    continue
                                    
                            if current_mem_mb > max_memory_mb:
                                max_memory_mb = current_mem_mb
                            
                            # Check memory limit
                            if step.memory_limit_mb and current_mem_mb > step.memory_limit_mb:
                                process.kill()
                                error_msg = f"Memory limit exceeded: {current_mem_mb:.2f}MB > {step.memory_limit_mb}MB"
                                logger.error(f"{log_prefix} {step.name} ... FAIL ({error_msg})")
                                stderr_output = error_msg
                                raise RuntimeError(error_msg)
                            
                            # Check memory warning
                            if step.memory_warn_mb and current_mem_mb > step.memory_warn_mb:
                                warn_msg = f"Memory usage warning: {current_mem_mb:.2f}MB > {step.memory_warn_mb}MB"
                                if warn_msg not in step_warnings:
                                    logger.warning(f"{log_prefix} {step.name} ... {warn_msg}")
                                    step_warnings.append(warn_msg)
                                
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            break
                        time.sleep(0.1)
                    
                    stdout_output, stderr_output = process.communicate()
                    exit_code = process.returncode
                    
                    if exit_code == 0:
                        logger.info(f"{log_prefix} {step.name} ... OK{attempt_prefix}")
                        step_status = "success"
                        success = True
                        break # Success, move to next step
                    else:
                        logger.error(f"{log_prefix} {step.name} ... FAIL{attempt_prefix}")
                        logger.error(f"Command '{step.command}' failed with exit code {exit_code}")
                        if stdout_output:
                            logger.error(f"--- stdout ---\n{stdout_output}")
                        if stderr_output:
                            logger.error(f"--- stderr ---\n{stderr_output}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"{log_prefix} {step.name} ... FAIL (Timeout after {step.timeout_seconds}s){attempt_prefix}")
                step_status = "failure"
                exit_code = 124 
                logger.error(f"Command '{step.command}' timed out")
            except Exception:
                logger.exception(f"{log_prefix} {step.name} ... ERROR: Failed to execute step '{step.name}'{attempt_prefix}")
                step_status = "failure"
            
        step_finished_at = datetime.now()
        duration = (step_finished_at - step_started_at).total_seconds()

        # For non-shell steps, command might be None, so we provide a placeholder
        recorded_command = step.command if step.command else f"{step.type} ({step.params.get('artifacts_dir', '.')})"

        step_results.append(StepResult(
            name=step.name,
            command=recorded_command,
            status=step_status,
            exit_code=exit_code,
            started_at=step_started_at,
            finished_at=step_finished_at,
            duration_seconds=duration,
            stdout=stdout_output,
            stderr=stderr_output,
            max_memory_mb=max_memory_mb,
            retry_count=attempt - 1,
            warnings=step_warnings
        ))

        if not success:
            pipeline_overall_status = "failure"
            break # Move to next step loop, which will break due to failure
            
    pipeline_finished_at = datetime.now()
    
    logger.info(f"Pipeline '{pipeline.name}' completed with status: {pipeline_overall_status}.")
    
    return PipelineResult(
        pipeline_name=pipeline.name,
        started_at=pipeline_started_at,
        finished_at=pipeline_finished_at,
        status=pipeline_overall_status,
        step_results=step_results
    )
