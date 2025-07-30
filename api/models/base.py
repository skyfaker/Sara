from sqlalchemy.orm import declarative_base

from models import metadata

Base = declarative_base(metadata=metadata)
