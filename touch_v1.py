from ppadb.client import Client as AdbClient
from PIL import Image
import pytesseract
import io

# Initialize ADB connection
def connect_device():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if len(devices) == 0:
        print("No device connected.")
        return None
    print("Device connected.")
    return devices[0]

# Capture screenshot and retrieve text within coordinates
def get_text_in_region(device, x1, y1, x2, y2):
    if device:
        # Capture screenshot
        screenshot = device.screencap()
        
        # Open the screenshot as an image
        image = Image.open(io.BytesIO(screenshot))
        
        # Crop the region from (x1, y1) to (x2, y2)
        region = image.crop((x1, y1, x2, y2))
        
        # Perform OCR on the cropped region
        text = pytesseract.image_to_string(region)
        print("Extracted text:", text)
        return text

# Connect to device and extract text
device = connect_device()
if device:
    text = get_text_in_region(device, x1=95, y1=98, x2=225, y2=125)
