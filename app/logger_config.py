import json
import logging

from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "log_type": record.name,
            "timestamp": self.formatTime(record),
            "level": record.levelname,
        }

        if has_request_context():
            log_record.update(
                {
                    "remote_addr": request.remote_addr,
                    "url": request.url,
                }
            )

        try:
            message_data = json.loads(record.getMessage())
            if isinstance(message_data, dict):
                log_record.update(message_data)
            else:
                log_record["message"] = message_data
        except json.JSONDecodeError:
            log_record["message"] = record.getMessage()

        return json.dumps(log_record)


def setup_logger(name, level, formatter):
    """Helper function to set up a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def setup_logging(app):
    """Set up loggers for the app."""
    audit_log_formatter = RequestFormatter()
    app.audit_logger = setup_logger(
        "audit_logger", logging.INFO, audit_log_formatter
    )

    app_log_formatter = RequestFormatter()
    app.app_logger = setup_logger("app_logger", logging.INFO, app_log_formatter)
