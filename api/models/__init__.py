"""
database engine and database models

Python的模块导入机制是延迟加载的，而SQLAlchemy在类定义时被执行到时才会把表信息注册到 metadata，
因此如果模型类没有被导入，其定义就不会被注册到 Base.metadata。
为了保证migrations命令执行时所有模型类被注册，因此在init中导入模型类

"""
from .database import db, metadata
from .model import UploadFile

__all__ = [
    "db",
    "metadata",
    "UploadFile"
]
