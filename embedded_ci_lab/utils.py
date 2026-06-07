import logging
import os
import sys

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "latest.log")

def setup_logging(log_file_path=None): # Added argument
    log_file_to_use = log_file_path if log_file_path else LOG_FILE
    log_dir_to_use = os.path.dirname(log_file_to_use)

    os.makedirs(log_dir_to_use, exist_ok=True)

    # Ensure logging is only configured once
    # Reset handlers to allow re-configuration in tests
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close() # Important to close

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_to_use, mode='w'), # Overwrite for latest.log
            logging.StreamHandler(sys.stdout)
        ]
    )