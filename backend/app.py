import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import fungsi kompresi
from compress_image import compress_dct_image
from compress_audio import compress_dct_audio
from compress_video import compress_video_tdt

# Setup Aplikasi Flask
app = Flask(__name__)
# Mengizinkan akses dari semua origin
CORS(app) 
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route untuk kompresi gambar
@app.route('/compress/image', methods=['POST'])
def compress_image_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    cutoff_level = int(request.form.get('cutoff_level', 75))
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = compress_dct_image(path, cutoff_level)
    os.remove(path)
    if result is None:
        return jsonify({"error": "Image compression failed"}), 500
    return jsonify(result)

# Route untuk kompresi audio
@app.route('/compress/audio', methods=['POST'])
def compress_audio_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    cutoff_level = int(request.form.get('cutoff_level', 95))
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = compress_dct_audio(path, cutoff_level)
    os.remove(path)
    if result is None:
        return jsonify({"error": "Audio compression failed"}), 500
    return jsonify(result)

# Route untuk kompresi video
@app.route('/compress/video', methods=['POST'])
def compress_video_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    cutoff_level = int(request.form.get('cutoff_level', 75))
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # =======================================================
    # PERBAIKAN: Simpan file DULU, baru dapatkan ukurannya.
    # =======================================================
    file.save(path)
    original_size = os.path.getsize(path)

    output_path = compress_video_tdt(path, cutoff_level)
    
    if output_path and os.path.exists(output_path):
        compressed_size = os.path.getsize(output_path)
        with open(output_path, 'rb') as f:
            video_bytes = f.read()
        
        base64_video = base64.b64encode(video_bytes).decode('utf-8')
        compression_ratio = 100 - ((compressed_size / original_size) * 100) if original_size > 0 else 0
        
        os.remove(output_path)
        os.remove(path)
        
        return jsonify({
            "video_base64": base64_video,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(compression_ratio, 2)
        })
    else:
        if os.path.exists(path):
            os.remove(path)
        return jsonify({"error": "Video compression failed. Check backend console for FFmpeg errors."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
