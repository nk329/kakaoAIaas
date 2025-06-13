from pydantic import BaseModel
from typing import List, Optional

class FileInfo(BaseModel):
    name: str
    size: int
    ext: str

class FileListResponse(BaseModel):
    total: int
    files: List[FileInfo] 