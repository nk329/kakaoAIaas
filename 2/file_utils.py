from fastapi import UploadFile, HTTPException
from typing import List, Optional
from pathlib import Path
import shutil
import os
import zipfile
from io import BytesIO
from schemas import FileInfo, FileListResponse

def save_upload_files(files: List[UploadFile], upload_dir: Path) -> List[FileInfo]:
    saved = []
    for file in files:
        dest = upload_dir / file.filename
        with dest.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved.append(FileInfo(name=file.filename, size=dest.stat().st_size, ext=dest.suffix))
    return saved

def get_file_list(upload_dir: Path, skip: int, limit: int, ext: Optional[str]) -> FileListResponse:
    all_files = [f for f in upload_dir.iterdir() if f.is_file()]
    if ext:
        all_files = [f for f in all_files if f.suffix == ("." + ext if not ext.startswith(".") else ext)]
    total = len(all_files)
    files = [FileInfo(name=f.name, size=f.stat().st_size, ext=f.suffix) for f in all_files[skip:skip+limit]]
    return FileListResponse(total=total, files=files)

def get_file_path(upload_dir: Path, name: str) -> Path:
    file_path = upload_dir / name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")
    return file_path

def delete_files(upload_dir: Path, names: List[str]) -> List[str]:
    deleted = []
    for name in names:
        file_path = upload_dir / name
        if file_path.exists():
            file_path.unlink()
            deleted.append(name)
    return deleted

def zip_files_stream(upload_dir: Path, names: List[str]):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for name in names:
            file_path = upload_dir / name
            if file_path.exists():
                zipf.write(file_path, arcname=name)
    zip_buffer.seek(0)
    return zip_buffer, "files.zip" 