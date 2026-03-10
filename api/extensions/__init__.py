"""
extensions for Components
"""
from .ext_blueprints import init_blueprints
from .ext_db import init_db
from .ext_logging import init_logging
from .ext_migrate import init_migrate
from .ext_storage import init_storage

# Export init_logging first
# ext list includes all extensions you want to be initialized in app_factory.py
ext = [
    init_logging,
    init_blueprints,
    init_db,
    init_migrate,
    init_storage
]

__all__ = ["ext"]
