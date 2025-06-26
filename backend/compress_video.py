import cv2
import numpy as np
import os

def compress_video(filepath):
    cap = cv2.VideoCapture(filepath)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path = 'compressed_video.avi'
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dct_frame = cv2.dct(np.float32(gray))
        dct_frame[30:, :] = 0
        dct_frame[:, 30:] = 0
        idct_frame = cv2.idct(dct_frame)
        color_frame = cv2.cvtColor(np.uint8(idct_frame), cv2.COLOR_GRAY2BGR)
        out.write(color_frame)
    cap.release()
    out.release()
    return output_path