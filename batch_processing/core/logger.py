import logging
import json
import sys

class JsonLoggingFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record: logging.LogRecord):
        json_record = {
            "message": record.msg,
            "time": record.created,
            "level": record.levelname,
            "file": record.filename,
            "func": record.funcName,
            "module": record.pathname,
        }
        formatted_record = json.dumps(json_record, sort_keys=True)
        return formatted_record

def setup_logger(log_file_path, logger_name):
    log_file_handler = logging.FileHandler(filename=log_file_path)
    log_file_handler.setFormatter(JsonLoggingFormatter())
    log_file_handler.setLevel(logging.INFO)

    log_stream_handler = logging.StreamHandler(sys.stdout)
    log_stream_handler.setFormatter(JsonLoggingFormatter())
    log_stream_handler.setLevel(logging.INFO)

    source_logger = logging.getLogger(logger_name)
    source_logger.setLevel(logging.INFO)
    source_logger.addHandler(log_stream_handler)
    return source_logger