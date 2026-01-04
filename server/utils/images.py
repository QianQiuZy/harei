import os
import uuid
from PIL import Image


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_image(file_storage, upload_dir: str) -> tuple[str, str]:
    _ensure_dir(upload_dir)
    _ensure_dir(os.path.join(upload_dir, "thumbs"))

    filename = f"{uuid.uuid4().hex}.jpg"
    full_path = os.path.join(upload_dir, filename)
    thumb_path = os.path.join(upload_dir, "thumbs", filename)

    image = Image.open(file_storage)
    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background
    else:
        image = image.convert("RGB")

    image.save(full_path, format="JPEG", quality=80)

    thumb = image.copy()
    thumb.thumbnail((320, 320))
    thumb.save(thumb_path, format="JPEG", quality=80)

    return full_path, thumb_path
