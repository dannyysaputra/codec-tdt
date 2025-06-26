from flask import Flask, request, send_file
from compress_image import compress_dct_image
from compress_audio import compress_fft_audio
from compress_video import compress_video
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/compress/*": {"origins": "*"}})
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/compress/image', methods=['POST'])
def compress_image():
    file = request.files['file']
    cutoff = int(request.form.get('cutoff', 30))  # default: 30
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    result = compress_dct_image(path, cutoff)
    return {
        "compressed_image": result["image_base64"],
        "compression_ratio": result["compression_ratio"]
    }

@app.route('/compress/audio', methods=['POST'])
def compress_audio():
    file = request.files['file']
    cutoff = int(request.form.get('cutoff', 5000))  # default 5KHz
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    result = compress_fft_audio(path, cutoff)
    return {
        "compressed_audio": result["audio_base64"],
        "compression_ratio": result["compression_ratio"]
    }

@app.route('/compress/video', methods=['POST'])
def compress_vid():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    output = compress_video(path)
    return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)