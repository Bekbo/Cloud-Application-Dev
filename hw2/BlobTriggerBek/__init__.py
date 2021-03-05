import logging
import io
import sys
from PIL import Image
import azure.functions as func


def main(myblob: func.InputStream, myblobout: func.Out[bytes], context: func.Context):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    base_image = Image.open(myblob)
    in_mem_img = io.BytesIO()
    base_image.thumbnail((128,128), Image.ANTIALIAS)
    base_image.save(in_mem_img, format=base_image.format)
    myblobout.set(in_mem_img.getvalue())
    logging.info(f'Thumbnail success!')
