import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct

def compress_dct_image(filepath, cutoff_level):
    """
    Mengompresi gambar menggunakan TDT (DCT) dengan cutoff berbasis persentase.
    'cutoff_level' (1-99) menentukan persentase koefisien DCT
    yang paling tidak signifikan (detail halus) untuk dibuang.
    """
    try:
        # 1. Baca File dan Dapatkan Ukuran Asli
        original_size = os.path.getsize(filepath)
        with Image.open(filepath) as img:
            # Pastikan gambar dalam format RGB (tanpa alpha/transparansi)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            # Lakukan TDT pada channel Luminance (kecerahan) karena mata manusia
            # lebih peka terhadap perubahan kecerahan daripada warna.
            arr = np.array(img.convert('L'))
    except Exception as e:
        print(f"Error saat memuat gambar: {e}")
        return None

    # =================================================================
    #  PROSES TDT (TRANSFORM DOMAIN TECHNIQUE)
    # =================================================================

    # 2. Terapkan TDT (DCT) 2 Dimensi
    # Mengubah data dari domain spasial (piksel) ke domain frekuensi.
    dct_img = dct(dct(arr.T, norm='ortho').T, norm='ortho')

    # 3. Kuantisasi/Cutoff Berbasis Persentase
    # Ini adalah inti dari kompresi lossy.
    flat_coeffs = dct_img.flatten()
    num_coeffs_to_zero = int(len(flat_coeffs) * (cutoff_level / 100.0))
    # Dapatkan indeks dari koefisien dengan magnitudo (nilai absolut) terkecil.
    indices_to_zero = np.argsort(np.abs(flat_coeffs))[:num_coeffs_to_zero]
    # Jadikan nol koefisien-koefisien tersebut.
    flat_coeffs[indices_to_zero] = 0
    # Bentuk kembali matriks DCT yang sudah disederhanakan.
    dct_img = flat_coeffs.reshape(dct_img.shape)
    
    # 4. Terapkan Inverse TDT (IDCT) 2 Dimensi
    # Mengubah kembali data dari domain frekuensi ke domain spasial.
    idct_img = idct(idct(dct_img.T, norm='ortho').T, norm='ortho')
    result_img = Image.fromarray(np.clip(idct_img, 0, 255).astype(np.uint8))

    # =================================================================
    #  PENYIMPANAN & PENGEMBALIAN HASIL
    # =================================================================

    # 5. Simpan sebagai JPEG untuk mendapatkan kompresi nyata.
    # Format JPEG secara internal juga menggunakan TDT dan entropy-coding,
    # sehingga ukuran file bisa menjadi sangat kecil.
    compressed_buffer = BytesIO()
    result_img.save(compressed_buffer, format="JPEG", quality=85) # Kualitas 85 adalah kompromi yang baik.
    compressed_size = len(compressed_buffer.getvalue())

    # Encode ke base64 untuk dikirim via JSON.
    base64_result = base64.b64encode(compressed_buffer.getvalue()).decode('utf-8')
    
    # Hitung rasio pengurangan ukuran.
    compression_ratio = 100 - ((compressed_size / original_size) * 100) if original_size > 0 else 0

    return {
        "image_base64": base64_result,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": round(compression_ratio, 2)
    }
