from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from typing import List, Optional
from pathlib import Path
import shutil
import os
import zipfile
from schemas import FileInfo, FileListResponse
from file_utils import (
    save_upload_files, get_file_list, delete_files, get_file_path, zip_files_stream
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="멀티 파일 관리 API")

@app.post("/upload", response_model=List[FileInfo])
def upload_files(files: List[UploadFile] = File(...)):
    return save_upload_files(files, UPLOAD_DIR)

@app.get("/files", response_model=FileListResponse)
def list_files(
    skip: int = 0, limit: int = 10, ext: Optional[str] = Query(None, description="확장자 필터")
):
    return get_file_list(UPLOAD_DIR, skip, limit, ext)

@app.get("/download")
def download_files(names: List[str] = Query(..., description="다운로드할 파일명 리스트")):
    if len(names) == 1:
        file_path = get_file_path(UPLOAD_DIR, names[0])
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")
        return FileResponse(file_path, filename=names[0], media_type="application/octet-stream")
    else:
        zip_stream, zip_name = zip_files_stream(UPLOAD_DIR, names)
        return StreamingResponse(zip_stream, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={zip_name}"})

@app.delete("/files", response_model=List[str])
def delete_files_api(names: List[str] = Query(..., description="삭제할 파일명 리스트")):
    return delete_files(UPLOAD_DIR, names) 