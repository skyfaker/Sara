import logging
import os
import sys
from logging.handlers import RotatingFileHandler
import uuid
import flask

from configs import app_config


def init_logging(app: flask.Flask):
    log_handlers: list[logging.Handler] = []
    log_file = app_config.LOG_FILE
    if log_file:
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
        log_handlers.append(
            RotatingFileHandler(
                filename=log_file,
                maxBytes=app_config.LOG_FILE_MAX_SIZE * 1024 * 1024,
                backupCount=app_config.LOG_FILE_BACKUP_COUNT,
            )
        )

    # Always add StreamHandler to log to console
    sh = logging.StreamHandler(sys.stdout)
    log_handlers.append(sh)

    # Apply RequestIdFilter to all handlers
    for handler in log_handlers:
        handler.addFilter(RequestIdFilter())

    logging.basicConfig(
        level=app_config.LOG_LEVEL,
        format=app_config.LOG_FORMAT,
        datefmt=app_config.LOG_DATEFORMAT,
        handlers=log_handlers,
        force=True,
    )


def get_request_id():
    if getattr(flask.g, "request_id", None):
        return flask.g.request_id

    new_uuid = uuid.uuid4().hex[:10]
    flask.g.request_id = new_uuid

    return new_uuid


class RequestIdFilter(logging.Filter):
    # This is a logging filter that makes the request ID available in the logging format.
    #  We're checking if we're in a request context,
    #  as we may want to log things before Flask is fully loaded.
    def filter(self, record):
        record.req_id = get_request_id() if flask.has_request_context() else ""
        return True


class RequestIdFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "req_id"):
            record.req_id = ""
        return super().format(record)


def apply_request_id_formatter():
    for handler in logging.root.handlers:
        if handler.formatter:
            handler.formatter = RequestIdFormatter(app_config.LOG_FORMAT, app_config.LOG_DATEFORMAT)
