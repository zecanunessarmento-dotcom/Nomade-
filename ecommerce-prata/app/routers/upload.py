import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
def upload_image(
    file: UploadFile = File(...)
):
    upload_dir = Path("uploads")

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "filename": file.filename,
        "url": f"/uploads/{file.filename}"
    }