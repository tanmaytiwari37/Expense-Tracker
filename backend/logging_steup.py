import logging
import os
import sys

# Create a custom logger
def setup_logger(name, log_file='server.log'):
    
    logger_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
    logger = logging.getLogger(name)
    # Configure the custom logger
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(logger_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger