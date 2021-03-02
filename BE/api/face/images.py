import tempfile
from typing import Tuple
from PIL import Image



class ImageException(Exception):
    def __init__(self, messages: str) -> None:
        self.messages = messages


def _reorient_image(im: Image) -> Image:
    """
    Reorient images
    https://github.com/ageitgey/face_recognition/wiki/Common-Errors#issue-its-not-detecting-faces-in-my-very-simple-image-i-took-with-my-iphone--android-phone

    :param im: Pillow Image object
    :return: Pillow Image object that has proper image oreientation.
    """
    try:
        image_exif = im._getexif()
        image_orientation = image_exif[274]
        if image_orientation in (2, "2"):
            return im.transpose(Image.FLIP_LEFT_RIGHT)
        elif image_orientation in (3, "3"):
            return im.transpose(Image.ROTATE_180)
        elif image_orientation in (4, "4"):
            return im.transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (5, "5"):
            return im.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (6, "6"):
            return im.transpose(Image.ROTATE_270)
        elif image_orientation in (7, "7"):
            return im.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (8, "8"):
            return im.transpose(Image.ROTATE_90)
        else:
            return im.save()
    except (KeyError, AttributeError, TypeError, IndexError):
        return im


def resize_and_reorient(file: str) -> Image:
    """
    Verifies a given file is an image, Reorients the image and rescales it.
    """
    try:
        image = Image.open(file.name)
        image = _reorient_image(image)
        max_size = (1000, 1000)
        image.thumbnail(max_size)
        return image
    except Exception as e:
        print(e)
        raise ImageException(('Error manipulating Images', e))
