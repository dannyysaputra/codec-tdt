# Buat WAV asli dari sample untuk mendapatkan ukuran file yang adil
from pydub import AudioSegment
from io import BytesIO
import base64
import numpy as np
from scipy.fft import rfft, irfft

def compress_fft_audio(filepath, cutoff=5000):
    if filepath.lower().endswith(".mp3"):
        audio = AudioSegment.from_mp3(filepath)
    else:
        audio = AudioSegment.from_file(filepath)

    audio = audio.set_channels(1).set_sample_width(2)
    samples = np.array(audio.get_array_of_samples())
    samplerate = audio.frame_rate

    # Simpan audio asli sebagai WAV untuk dapatkan ukurannya
    original_buffer = BytesIO()
    audio.export(original_buffer, format="wav")
    original_size = len(original_buffer.getvalue())

    # FFT kompresi
    transformed = rfft(samples)
    transformed[cutoff:] = 0
    compressed = irfft(transformed).astype(np.int16)

    # Simpan hasil kompresi
    compressed_buffer = BytesIO()
    AudioSegment(
        compressed.tobytes(),
        frame_rate=samplerate,
        sample_width=2,
        channels=1
    ).export(compressed_buffer, format="wav")

    compressed_bytes = compressed_buffer.getvalue()
    compressed_size = len(compressed_bytes)

    compression_ratio = 100 - ((compressed_size / original_size) * 100)
    base64_audio = base64.b64encode(compressed_bytes).decode('utf-8')

    print(f"Original size: {original_size} bytes, Compressed size: {compressed_size} bytes, Compression ratio: {compression_ratio:.2f}%")

    return {
        "audio_base64": base64_audio,
        "compression_ratio": round(compression_ratio, 2)
    }