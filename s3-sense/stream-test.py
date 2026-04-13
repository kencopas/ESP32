import requests
import cv2
import numpy as np

STREAM_URL = "http://192.168.6.104:81/stream"

print("Connecting...")

stream = requests.get(STREAM_URL, stream=True, timeout=(5, None))

print("Connected.")

bytes_data = b""

for chunk in stream.iter_content(chunk_size=512):
    if not chunk:
        continue

    bytes_data += chunk

    a = bytes_data.find(b"\xff\xd8")
    b = bytes_data.find(b"\xff\xd9")

    if a != -1 and b != -1:
        jpg = bytes_data[a : b + 2]
        bytes_data = bytes_data[b + 2 :]

        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("ESP32 Stream", frame)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
