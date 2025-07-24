import logging
import time

from flask import Flask

from configs import app_config


def init_extensions(app: Flask):
    from extensions import __all__
    for init_func in __all__:
        init_func(app)


def create_app():
    start_time = time.perf_counter()
    app = Flask("SaRa")
    app.config.from_mapping(app_config.model_dump())
    init_extensions(app)
    end_time = time.perf_counter()
    if app_config.DEBUG:
        logging.info(f"Finished create_app ({round((end_time - start_time) * 1000, 2)} ms)")
    return app
