from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct
from io import BytesIO
import base64

def compress_dct_image(filepath, cutoff=30):
    img = Image.open(filepath).convert('L')
    arr = np.array(img)

    original_buffer = BytesIO()
    img.save(original_buffer, format="JPEG")
    original_size = len(original_buffer.getvalue())

    dct_img = dct(dct(arr.T, norm='ortho').T, norm='ortho')
    dct_img[cutoff:, :] = 0
    dct_img[:, cutoff:] = 0
    idct_img = idct(idct(dct_img.T, norm='ortho').T, norm='ortho')
    result = Image.fromarray(np.clip(idct_img, 0, 255).astype(np.uint8))

    compressed_buffer = BytesIO()
    result.save(compressed_buffer, format="JPEG")
    compressed_size = len(compressed_buffer.getvalue())
    base64_result = base64.b64encode(compressed_buffer.getvalue()).decode('utf-8')

    compression_ratio = 100 - ((compressed_size / original_size) * 100)

    return {
        "image_base64": base64_result,
        "compression_ratio": round(compression_ratio, 2)
    }
