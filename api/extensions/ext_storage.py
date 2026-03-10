from enum import StrEnum
from flask import Flask
from configs import app_config


class StorageType(StrEnum):
    LOCAL = "local"


class Storage:
    def __init__(self):
        self.storage_runner = None

    @staticmethod
    def storage_factory(storage_type: str) -> type:
        match storage_type:
            case StorageType.LOCAL:
                from extensions.storage.local_storage import LocalStorage

                return LocalStorage
            case _:
                raise ValueError(f"unsupported storage type {storage_type}")

    def init_app(self, app: Flask):
        storage_class = self.storage_factory(app_config.STORAGE_TYPE)
        self.storage_runner = storage_class()
        app.extensions["storage"] = self.storage_runner

    def save(self, filename, data):
        self.storage_runner.save(filename, data)

    def load(self, filename: str):
        return self.storage_runner.load(filename)

    def download(self, filename, target_filepath):
        self.storage_runner.download(filename, target_filepath)

    def exists(self, filename):
        return self.storage_runner.exists(filename)

    def delete(self, filename):
        return self.storage_runner.delete(filename)


storage = Storage()


def init_storage(app: Flask):
    storage.init_app(app)
