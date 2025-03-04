import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
PROCESSED_FOLDER = os.path.join('static', 'processed')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # Save the uploaded image
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Process the image to remove the watermark
            processed_path = process_image(filepath, file.filename)
            return redirect(url_for("view_image", filename=file.filename))

    return render_template("index.html")

@app.route("/view/<filename>")
def view_image(filename):
    original_path = os.path.join('uploads', filename)
    processed_path = os.path.join('processed', filename)
    return render_template("view_image.html", original=original_path, processed=processed_path)

def process_image(filepath, filename):
    # Load the image
    image = cv2.imread(filepath)

    # Convert to grayscale to detect the watermark
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to create a binary mask of the watermark
    _, mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Save the mask for debugging
    mask_path = os.path.join(PROCESSED_FOLDER, f"mask_{filename}")
    cv2.imwrite(mask_path, mask)

    # Invert the mask to isolate the watermark region
    mask = cv2.bitwise_not(mask)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Apply inpainting to remove the watermark
    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

    # Save the processed image
    processed_path = os.path.join(PROCESSED_FOLDER, filename)
    cv2.imwrite(processed_path, inpainted_image)

    return processed_path


if __name__ == "__main__":
    app.run(debug=True)
