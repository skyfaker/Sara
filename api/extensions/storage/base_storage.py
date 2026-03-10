from abc import ABC, abstractmethod
from collections.abc import Generator


class BaseStorage(ABC):
    """Interface for file storage."""

    @abstractmethod
    def save(self, filename, data):
        raise NotImplementedError

    @abstractmethod
    def load(self, filename: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def download(self, filename, target_filepath):
        raise NotImplementedError

    @abstractmethod
    def exists(self, filename):
        raise NotImplementedError

    @abstractmethod
    def delete(self, filename):
        raise NotImplementedError
