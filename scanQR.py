from picamera2 import Picamera2
from pyzbar.pyzbar import decode, ZBarSymbol
import os
import time

os.environ["LIBCAMERA_LOG_LEVELS"] = "2"

def scanQR():
    with Picamera2() as picam2:
        picam2.start()
        start_time = time.time()
        while time.time() - start_time < 2:
            img = picam2.capture_array()
            decoded = decode(img, symbols=[ZBarSymbol.QRCODE])
            if decoded:
                print(decoded)
                
scanQR()
