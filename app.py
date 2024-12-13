# from flask import Flask, render_template, request, redirect, url_for
# import cv2
# import numpy as np
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # محاكاة تأثير الأشعة فوق البنفسجية (UV)
# def simulate_uv_effect(image_path):
#     image = cv2.imread(image_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     uv_image = image.copy()
#     uv_image[:, :, 0] = uv_image[:, :, 0] * 0.1  # تقليل القناة الحمراء
#     uv_image[:, :, 1] = uv_image[:, :, 1] * 0.3  # تقليل القناة الخضراء
#     uv_image[:, :, 2] = uv_image[:, :, 2] * 2.0  # تعزيز القناة الزرقاء
#     uv_image = np.clip(uv_image, 0, 255).astype(np.uint8)
#     return uv_image

# # كشف العلامات المائية باستخدام FFT
# def analyze_watermark(image_path):
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
#     # تطبيق FFT على الصورة
#     f = np.fft.fft2(image)
#     fshift = np.fft.fftshift(f)  # تحويل المركز إلى وسط الصورة
#     magnitude_spectrum = np.log(np.abs(fshift) + 1)

#     return magnitude_spectrum

# @app.route('/')
# def index():
#     return render_template('index.html')

# # صفحة تسجيل الدخول
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == "admin" and password == "1234":
#             return redirect(url_for('image_upload'))  # الانتقال لصفحة تحميل الصور
#         else:
#             return render_template('login.html', error="Invalid credentials. Please try again.")
#     return render_template('login.html')

# # صفحة تحميل الصور ومقارنة النتائج
# @app.route('/image_upload', methods=['GET', 'POST'])
# def image_upload():
#     if request.method == 'POST':
#         if 'file1' not in request.files or 'file2' not in request.files:
#             return "Please upload both images."

#         file1 = request.files['file1']
#         file2 = request.files['file2']

#         if file1 and file2:
#             file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
#             file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
#             file1.save(file1_path)
#             file2.save(file2_path)

#             # محاكاة الأشعة فوق البنفسجية على الصور
#             uv1 = simulate_uv_effect(file1_path)
#             uv2 = simulate_uv_effect(file2_path)

#             # حفظ الصور التي تم معالجتها
#             uv1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uv1.jpg')
#             uv2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uv2.jpg')
#             cv2.imwrite(uv1_path, cv2.cvtColor(uv1, cv2.COLOR_RGB2BGR))
#             cv2.imwrite(uv2_path, cv2.cvtColor(uv2, cv2.COLOR_RGB2BGR))

#             # تحليل العلامات المائية
#             watermark_analysis_1 = analyze_watermark(file1_path)
#             watermark_analysis_2 = analyze_watermark(file2_path)

#             # حفظ تحليلات العلامات المائية
#             watermark_1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark_analysis_1.jpg')
#             watermark_2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark_analysis_2.jpg')
#             cv2.imwrite(watermark_1_path, watermark_analysis_1)
#             cv2.imwrite(watermark_2_path, watermark_analysis_2)

#             return render_template('image_upload.html', 
#                                    uv1=uv1_path, 
#                                    uv2=uv2_path, 
#                                    watermark_1=watermark_1_path, 
#                                    watermark_2=watermark_2_path)

#     return render_template('image_upload.html')

# if __name__ == '__main__':

#     app.run(debug=True)