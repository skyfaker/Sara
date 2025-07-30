from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .database import db


class UploadFile(Base):
    __tablename__ = "upload_files"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="upload_file_pkey"),
    )

    id: Mapped[str] = db.Column(db.String(255), server_default=db.text("uuid_generate_v4()"))
    tenant_id: Mapped[str] = db.Column(db.String(255), nullable=False)
    storage_type: Mapped[str] = db.Column(db.String(255), nullable=False)
    key: Mapped[str] = db.Column(db.String(255), nullable=False)
    name: Mapped[str] = db.Column(db.String(255), nullable=False)
    size: Mapped[int] = db.Column(db.Integer, nullable=False)
    extension: Mapped[str] = db.Column(db.String(255), nullable=False)
    mime_type: Mapped[str] = db.Column(db.String(255), nullable=True)
    created_by_role: Mapped[str] = db.Column(
        db.String(255), nullable=False, server_default=db.text("'account'::character varying")
    )
    created_by: Mapped[str] = db.Column(db.String(255), nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, nullable=False, server_default=func.current_timestamp())
    used: Mapped[bool] = db.Column(db.Boolean, nullable=False, server_default=db.text("false"))
    used_by: Mapped[str | None] = db.Column(db.String(255), nullable=True)
    used_at: Mapped[datetime | None] = db.Column(db.DateTime, nullable=True)
    hash: Mapped[str | None] = db.Column(db.String(255), nullable=True)
    source_url: Mapped[str] = mapped_column(sa.TEXT, default="")
