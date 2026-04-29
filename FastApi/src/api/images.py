import os

from fastapi import APIRouter, UploadFile
import shutil
from src.tasks.tasks import compress_image

router = APIRouter(prefix="/images", tags=["Hotel Images"])


@router.post("")
def upload_image(file: UploadFile):
    image_path = os.path.abspath(f"src/static/images/{file.filename}")
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    compress_image.delay(image_path)
