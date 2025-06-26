import base64
from io import BytesIO
from pydub import AudioSegment
import numpy as np
from scipy.fftpack import dct, idct

def compress_dct_audio(filepath, cutoff_level):
    """
    Mengompresi audio menggunakan TDT (DCT) dan menyimpannya sebagai MP3.
    'cutoff_level' (1-99) dipetakan ke bitrate MP3 untuk menjamin ukuran file lebih kecil.
    """
    try:
        audio = AudioSegment.from_file(filepath)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None

    # Standarisasi audio
    audio = audio.set_channels(1).set_sample_width(2)
    samples = np.array(audio.get_array_of_samples())
    
    original_buffer = BytesIO()
    audio.export(original_buffer, format="wav")
    original_size = len(original_buffer.getvalue())

    # Proses TDT/DCT (sebagai demonstrasi teknik)
    if len(samples) > 0:
        transformed = dct(samples, norm='ortho')
        num_coeffs_to_zero = int(len(transformed) * (cutoff_level / 100.0))
        indices_to_zero = np.argsort(np.abs(transformed))[:num_coeffs_to_zero]
        transformed[indices_to_zero] = 0
        compressed_samples = idct(transformed, norm='ortho').astype(np.int16)
        
        # Buat audio baru dari sampel yang diproses
        processed_audio = AudioSegment(
            compressed_samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=2,
            channels=1
        )
    else:
        processed_audio = audio

    # Peta 'cutoff_level' ke bitrate MP3 (misal 32kbps hingga 192kbps)
    # Tingkat kompresi tinggi (cutoff_level tinggi) -> bitrate rendah
    # Ini adalah kunci untuk mengurangi ukuran file secara nyata
    bitrate = str(int(192 - (cutoff_level / 99.0) * 160)) + "k"

    # Ekspor ke MP3 untuk kompresi sebenarnya
    compressed_buffer = BytesIO()
    processed_audio.export(compressed_buffer, format="mp3", bitrate=bitrate)
    
    compressed_size = len(compressed_buffer.getvalue())
    base64_audio = base64.b64encode(compressed_buffer.getvalue()).decode('utf-8')
    compression_ratio = 100 - ((compressed_size / original_size) * 100) if original_size > 0 else 0

    return {
        "audio_base64": base64_audio,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": round(compression_ratio, 2)
    }
