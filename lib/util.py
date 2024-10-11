import mimetypes
from base64 import b64decode, b64encode
from io import BytesIO

from PIL import Image


def base64_decode_image_data_url(data_url: str) -> Image:
    _, data = data_url.split("base64,", maxsplit=1)
    byte_data = b64decode(data)
    return Image.open(BytesIO(byte_data))


def base64_encode_image_file(image_file: BytesIO) -> str:
    file_type = image_file.type
    if not file_type:
        file_type = mimetypes.guess_type(image_file.name)[0]
    file_data = image_file.read()
    b64 = b64encode(file_data).decode("utf-8")
    return f"data:{file_type};base64,{b64}"
