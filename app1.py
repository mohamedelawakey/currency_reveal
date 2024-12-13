from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key"

# Folder configurations
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route: Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "1234":
            return redirect(url_for('image_upload'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')

# Route: Image Upload and Comparison Page
@app.route('/upload', methods=['GET', 'POST'])
def image_upload():
    if request.method == 'POST':
        if 'original' not in request.files or 'comparison' not in request.files:
            flash('Both images are required!')
            return redirect(request.url)

        original_file = request.files['original']
        comparison_file = request.files['comparison']

        if original_file and allowed_file(original_file.filename) and comparison_file and allowed_file(comparison_file.filename):
            original_filename = secure_filename(original_file.filename)
            comparison_filename = secure_filename(comparison_file.filename)

            original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            comparison_path = os.path.join(app.config['UPLOAD_FOLDER'], comparison_filename)

            original_file.save(original_path)
            comparison_file.save(comparison_path)

            # Process images
            uv_original = simulate_uv_effect(original_path)
            uv_comparison = simulate_uv_effect(comparison_path)

            # Compare UV images
            uv_difference = compute_uv_difference(uv_original, uv_comparison)

            # Analyze watermarks using FFT
            uv_watermark_original = analyze_watermark_fft(original_path)
            uv_watermark_comparison = analyze_watermark_fft(comparison_path)

            # Save the watermark results
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'original_watermark.png'), uv_watermark_original)
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'comparison_watermark.png'), uv_watermark_comparison)

            return render_template(
                'image_upload.html',
                original_image=original_filename,
                comparison_image=comparison_filename,
                uv_difference_image=save_result_image(uv_difference),
                watermark_original='original_watermark.png',
                watermark_comparison='comparison_watermark.png'
            )
        else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)

    return render_template('image_upload.html')

# Helper function: Simulate UV effect
def simulate_uv_effect(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    if len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Enhance blue channel to mimic UV
    uv_image = image.copy()
    uv_image[:, :, 0] *= 0.1  # Reduce red channel
    uv_image[:, :, 1] *= 0.3  # Reduce green channel
    uv_image[:, :, 2] *= 2.0  # Enhance blue channel

    return uv_image

# Helper function: Compute UV difference
def compute_uv_difference(uv1, uv2):
    uv1_gray = cv2.cvtColor(uv1, cv2.COLOR_BGR2GRAY)
    uv2_gray = cv2.cvtColor(uv2, cv2.COLOR_BGR2GRAY)
    if uv1_gray.shape != uv2_gray.shape:
        uv2_gray = cv2.resize(uv2_gray, uv1_gray.shape[::-1])

    return cv2.absdiff(uv1_gray, uv2_gray)

# Helper function: Save the result image
def save_result_image(image):
    result_filename = 'result.png'
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
    cv2.imwrite(result_path, image)
    return result_filename

# Helper function: Analyze watermark using FFT
def analyze_watermark_fft(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None

    # Apply FFT
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))

    return magnitude_spectrum

# Route: Static files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)