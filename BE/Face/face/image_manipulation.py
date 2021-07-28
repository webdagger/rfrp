import os
from typing import Tuple

from exceptions import ImageManipulationError
from PIL import Image


class ImageManipulation:
    """
    A class used to create thumbnails and manipulate the exif orientation of a directory of images.
        It checks and adjusts the rotation before creating the thumbnail.

    ...

    Methods
    -------
    manipulate()
        Method walks the images directory, reorients all the images and creates a '01.thumbnail.jpg' in the directory.
    """

    def __init__(self, images_directory: str) -> None:
        """
        Parameters
        ----------
        :param images_directory : str
            The directory where the images are located.
        """
        self.images_directory: str = images_directory

    def manipulate(self) -> None:
        """
        Method walks the images directory, reorients all the images and creates a '01.thumbnail.jpg' in the directory.

        Note
        ____
        This is used for all the 01.jpg images in a directory.
        Raises
        ------
        ImageManipulationError
            Raises if there is any error attempting to use the manipulate method.
        """
        try:
            for root, dirs, files in os.walk(self.images_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_directory = os.path.dirname(file_path)
                    if file_path.lower().endswith("01.jpg".lower()):
                        im: Image = Image.open(file_path)
                        im = _reorient_image(im)
                        im = _create_thumbnails(im)
                        im.save(f"{file_directory}/01.thumbnail.jpg")
                        return Image.open(f"{file_directory}/01.thumbnail.jpg")
        except Exception as e:
            raise ImageManipulationError(e)


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
            return im
    except (KeyError, AttributeError, TypeError, IndexError):
        return im


def _create_thumbnails(im: Image, thumb_size: Tuple = (1000, 1000)) -> Image:
    """
    Create 1000x1000 thumbnails.

    :param im: Pillow Image object
    :param thumb_size: Tuple containing the size the final thumbnail should be defaults as (200, 200)
    :return: Pillow Image object that has thumb_size applied with Image.thumbnail
    """
    im.thumbnail(thumb_size)
    return im


def oriented_thumbnail(im: Image) -> Image:
    """
    :params im: A PIL image
    :returns: A PIL image file that has reorient_image and create_thumbnail applied on it

    """
    image = _reorient_image(im)
    image = _create_thumbnails(image)
    return image
