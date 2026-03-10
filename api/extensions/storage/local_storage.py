import os

from configs import app_config
from extensions.storage.base_storage import BaseStorage


class LocalStorage(BaseStorage):
    def __init__(self):
        super().__init__()
        if app_config.LOCAL_STORAGE_PATH is None:
            raise ValueError("STORAGE_LOCAL_PATH is not set")
        self.root = app_config.LOCAL_STORAGE_PATH
        if not os.path.exists(self.root):
            os.makedirs(self.root)

    def save(self, filename, data):
        if self.exists(filename):
            raise FileExistsError(f"File {filename} already exists in local storage.")
        file_path = os.path.join(self.root, filename)
        
        # Ensure subdirectories exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as file:
            file.write(data)

    def load(self, filename: str) -> bytes:
        pass

    def download(self, filename, target_filepath):
        pass

    def exists(self, filename):
        if os.path.exists(os.path.join(self.root, filename)):
            return True
        return False

    def delete(self, filename):
        pass
