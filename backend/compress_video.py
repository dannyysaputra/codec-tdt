import ffmpeg
import os

def compress_video_tdt(filepath, cutoff_level):
    """
    Mengompresi video menggunakan FFmpeg. Codec H.264 (libx264)
    secara internal menggunakan TDT (DCT), menjadikannya implementasi
    TDT yang canggih dan efisien.
    
    'cutoff_level' (1-99) dipetakan ke CRF (Constant Rate Factor).
    CRF yang lebih tinggi = kompresi lebih tinggi, kualitas lebih rendah.
    """
    if not os.path.exists(filepath):
        print(f"Error: Input file not found at {filepath}")
        return None

    base, _ = os.path.splitext(os.path.basename(filepath))
    output_path = f"compressed_tdt_{base}.mp4"

    # Peta 'cutoff_level' ke CRF (misal rentang CRF 18-40)
    # cutoff_level 1 -> CRF 18 (kualitas sangat tinggi)
    # cutoff_level 99 -> CRF 40 (kualitas sangat rendah)
    crf_value = int(18 + (cutoff_level / 99.0) * 22)
    
    print(f"Starting video compression for: {filepath}")
    print(f"Using CRF value: {crf_value}")

    try:
        (
            ffmpeg
            .input(filepath)
            .output(output_path, vcodec='libx264', crf=crf_value, preset='fast')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"FFmpeg compression successful. File saved to {output_path}")
        return output_path
    except ffmpeg.Error as e:
        print('ffmpeg stdout:', e.stdout.decode('utf8'))
        print('ffmpeg stderr:', e.stderr.decode('utf8'))
        if os.path.exists(output_path):
            os.remove(output_path)
        return None