import time
from ppadb.client import Client as AdbClient
from PIL import Image
import pytesseract
import io

def connect_device():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if len(devices) == 0:
        print("No device connected.")
        return None
    print("Device connected.")
    return devices[0]

def get_text_in_region(device, x1, y1, x2, y2):
    screenshot = device.screencap()
    image = Image.open(io.BytesIO(screenshot))
    region = image.crop((x1, y1, x2, y2))
    text = pytesseract.image_to_string(region, config="--oem 3 --psm 7")
    return text

# Connect to device
device = connect_device()

# Continuous reading every 1.5 seconds
if device:
    while True:
        text = get_text_in_region(device, x1=95, y1=98, x2=225, y2=125)
        print("Extracted text:", text)
        time.sleep(1.5)
