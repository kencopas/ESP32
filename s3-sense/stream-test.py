import requests
import cv2
import numpy as np


STREAM_URL = "http://192.168.6.104:81/stream"

stream = requests.get(STREAM_URL, stream=True)
bytes_data = b""


for chunk in stream.iter_content(chunk_size=1024):
    bytes_data += chunk

    # Find JPEG start/end markers
    start = bytes_data.find(b"\xff\xd8")  # JPEG start
    end = bytes_data.find(b"\xff\xd9")  # JPEG end

    if start != -1 and end != -1:
        jpg = bytes_data[start : end + 2]
        bytes_data = bytes_data[end + 2 :]

        # Decode JPEG → image
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("ESP32 Stream", frame)

        # Press ESC to exit
        if cv2.waitKey(1) == 27:
            break


cv2.destroyAllWindows()
