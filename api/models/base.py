from sqlalchemy.orm import declarative_base

from models.database import metadata

Base = declarative_base(metadata=metadata)
