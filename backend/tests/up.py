from src.services.dropbox_service import DropboxService
from dataclasses import dataclass
import os

service = DropboxService()


@dataclass
class File:
    path: str


item = File(path="/item/gc.deb")


with open("gc.deb", "rb") as f:
    file_size = os.path.getsize("gc.deb")
    service.buffer_upload(item, f, file_size)
