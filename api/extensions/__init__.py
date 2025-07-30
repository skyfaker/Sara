"""
extensions for Components
"""
from .ext_blueprints import init_blueprints
from .ext_db import init_db
from .ext_logging import init_logging
from .ext_migrate import init_migrate

# Export init_logging first
__all__ = [
    init_logging,
    init_blueprints,
    init_db,
    init_migrate
]
