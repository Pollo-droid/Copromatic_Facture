import os
import time
import uuid
import cv2
import numpy as np
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from pdf2image import convert_from_bytes
import io
from API.Backend.config import TEMP_IMAGE_DIR

def setup_temp_directory(app):
    os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)
    app.mount("/temp_images", StaticFiles(directory=TEMP_IMAGE_DIR), name="temp_images")

async def cleanup_old_images():
    current_time = time.time()
    for filename in os.listdir(TEMP_IMAGE_DIR):
        file_path = os.path.join(TEMP_IMAGE_DIR, filename)
        try:
            if os.path.isfile(file_path) and os.path.getmtime(file_path) < current_time - 3600:
                os.remove(file_path)
                print(f"Removed old temporary file: {filename}")
        except Exception as e:
            print(f"Error removing file {filename}: {str(e)}")
    print("Cleanup of old temporary images completed")

import cv2
import numpy as np
from fastapi import UploadFile, HTTPException

async def handle_file_upload(file: UploadFile) -> np.ndarray:
    """
    Handles file upload for PNG images, reads the file, and performs basic preprocessing.

    Args:
        file (UploadFile): The uploaded file object

    Returns:
        np.ndarray: Processed OpenCV image

    Raises:
        HTTPException: If there are issues reading or processing the file
    """
    try:
        # Read the contents of the uploaded file
        contents = await file.read()

        # Convert the file contents to a numpy array
        nparr = np.frombuffer(contents, np.uint8)

        # Decode the image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Check if image was successfully loaded
        if img is None:
            raise HTTPException(status_code=400, detail="Failed to read the image file")

        return img

    except Exception as e:
        # Catch any unexpected errors during file processing
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
