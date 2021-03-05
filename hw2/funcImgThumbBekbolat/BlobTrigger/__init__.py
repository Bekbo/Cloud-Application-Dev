import logging
import io
from PIL import Image

import azure.functions as func

def main(myblob: func.InputStream, blobout: func.Out[bytes], context: func.Context):
    logging.info(f"Python blob trigger function processed blob \n"
                f"Name: {myblob.name}\n"
                f"Blob Size: {myblob.length} bytes")
    image = Image.open(myblob)
    in_memory_file = io.BytesIO()
    image.thumbnail((128,128), Image.ANTIALIAS)
    image.save(in_memory_file, format=image.format)
    thumbnail = in_memory_file.getvalue()
    blobout.set(thumbnail)

    logging.info(f"Thumbnail success")
