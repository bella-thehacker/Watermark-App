import os
from flask import Blueprint, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from App.models import Image
from App import db
from App.utils import remove_watermark

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return "No file uploaded", 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Process image to remove watermark
            processed_path = os.path.join(PROCESSED_FOLDER, filename)
            remove_watermark(filepath, processed_path)

            # Save to database
            image = Image(filename=filename)
            db.session.add(image)
            db.session.commit()

            return redirect(url_for('main.view_image', filename=filename))

    return render_template('index.html')


@main.route('/images/<filename>')
def view_image(filename):
    return render_template('view_image.html', filename=filename)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@main.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)
