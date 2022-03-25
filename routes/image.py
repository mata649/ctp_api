from fastapi import APIRouter, Body, File, Path, Query, HTTPException, Depends, UploadFile
from dotenv import load_dotenv
import os
from auth.jwt import JWTHandler
from schemas.image import ImageIn
from pyimgur import Imgur
import uuid
import base64
image = APIRouter(prefix='/image', tags=["Image"])
jwt_handler = JWTHandler()
load_dotenv()


@image.post("/")
def upload_image(my_file: bytes = File(...), current_id=Depends(jwt_handler.auth_wrapper)):
    imgur_client = Imgur(os.getenv("IMGUR_CLIENT_ID"))
    image_uuid =str(uuid.uuid1())
    image_path = os.path.join(os.getcwd(), "image",
                              f'{image_uuid}.jpg')
    with open(image_path, "wb") as f:
        f.write(my_file)
    uploaded_image = imgur_client.upload_image(path=image_path, title=image_uuid)
    os.remove(image_path)
    return {"image_url": uploaded_image.link_large_thumbnail}
