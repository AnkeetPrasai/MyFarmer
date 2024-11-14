import time
import re
from ppadb.client import Client as AdbClient
from PIL import Image, ImageOps
import pytesseract
import io
import numpy as np

# Connect to ADB device
def connect_device():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if len(devices) == 0:
        print("No device connected.")
        return None
    print("Device connected.")
    return devices[0]

def preprocess_image_for_color(image, target_hex="#eef8d5", tolerance=30):
    # Convert hex to RGB
    target_color = Image.new("RGB", (1, 1), target_hex).getpixel((0, 0))
    
    # Ensure the image is in RGB format
    image = image.convert("RGB")
    
    # Convert image to numpy array
    image_np = np.array(image)
    
    # Calculate the color difference
    diff = np.sqrt(np.sum((image_np - target_color) ** 2, axis=-1))
    
    # Create a mask for pixels within the tolerance range
    mask = diff < tolerance
    
    # Apply mask: set matching areas to white and others to black
    image_np[~mask] = [0, 0, 0]
    image_np[mask] = [255, 255, 255]
    
    # Convert back to PIL image and return
    return Image.fromarray(image_np)


# Extract only numeric text from OCR result
def get_numeric_text(region):
    text = pytesseract.image_to_string(region, config="--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789")
    numeric_text = ''.join(re.findall(r'\d+', text))  # Keep only digits
    return int(numeric_text) if numeric_text.isdigit() else 0

# Perform action based on extracted number
def process_text_value(device, value):
    if value > 1200000:
        # Play a notification
        print("value high")
        return True
    elif value == 0:
        return False
    else:
        # Simulate a touch if below 1.2 million
        device.shell(f"input tap 1450 520")
        print("Touch simulated")
        return False
        


# Extract text in region and process based on value
def get_text_in_region_and_process(device, x1, y1, x2, y2):
    screenshot = device.screencap()
    image = Image.open(io.BytesIO(screenshot))
    region = image.crop((x1, y1, x2, y2))
    
    # Preprocess the region to filter out non-matching colors
    preprocessed_region = preprocess_image_for_color(region, target_hex="#eef8d5", tolerance=30)
    
    # Extract numeric text from the preprocessed image
    numeric_value = get_numeric_text(preprocessed_region)
    print("Extracted number:", numeric_value)
    if (process_text_value(device, numeric_value) == True):
        return True

# Function that checks if were in home?
def home_check(device,x1,y1,x2,y2):
    screenshot = device.screencap()
    


# Connect to device
device = connect_device()

# Continuous reading every 1.5 seconds
if device:
    while True:
        if (get_text_in_region_and_process(device, x1=95, y1=98, x2=225, y2=125) == True):
            break
        time.sleep(1.5)
