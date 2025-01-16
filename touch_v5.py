import time
import re
from ppadb.client import Client as AdbClient
from PIL import Image, ImageOps
import pytesseract
import io
import numpy as np
import random

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


def simulate_perimeter_touches(device, num_points=20):
    """
    Simulates touches along diamond perimeter with natural variance
    """
    # Define diamond corners
    left_edge = (180, 470)
    top_point = (775, 80)  # Midpoint x of screen
    right_edge = (1370, 470)
    
    def get_random_point_on_line(start, end, progress):
        # Get point on line with some random variance
        base_x = start[0] + (end[0] - start[0]) * progress
        base_y = start[1] + (end[1] - start[1]) * progress
        
        # Calculate perpendicular vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = (dx**2 + dy**2)**0.5
        perp_x = -dy/length
        perp_y = dx/length
        
        # Add random variance (max 30 pixels from perimeter)
        variance = random.randint(-40, 40)
        x = int(base_x + perp_x * variance)
        y = int(base_y + perp_y * variance)
        
        return x, y
    
    # Generate points along left-to-top edge
    for i in range(num_points):
        progress = i / (num_points - 1)
        x, y = get_random_point_on_line(left_edge, top_point, progress)
        device.shell(f"input tap {x} {y}")
        time.sleep(random.uniform(0.1, 0.3))  # Random delay between taps
    
    # Generate points along top-to-right edge
    for i in range(num_points):
        progress = i / (num_points - 1)
        x, y = get_random_point_on_line(top_point, right_edge, progress)
        device.shell(f"input tap {x} {y}")
        time.sleep(random.uniform(0.1, 0.3))

def simulate_swipe(device):
    # Random x position between 400 and 900
    x_pos = random.randint(400,900)
    x_pos1 = x_pos + random.randint(-15,15)
    y_pos = random.randint(190,240)
    y_pos1 = random.randint(290,400)
    swipe_time = random.randint(260,400)
    device.shell(f"input swipe {x_pos} {y_pos} {x_pos1} {y_pos1} {swipe_time}")

def attack(device):
    """
    Main attack function that coordinates the attack sequence
    """
    print("Enter 1 to attack, any other key to skip: ")
    choice = input()
    
    if choice != "1":
        device.shell(f"input tap {random.randint(1350,1540)} {random.randint(475,550)}")
        return
    
    # Initial press on 1st troop box
    press_x = random.randint(260, 330)
    press_y = random.randint(600, 700)
    device.shell(f"input tap {press_x} {press_y}")
    time.sleep(random.uniform(0.5, 1.0))
    
    simulate_swipe(device)
    simulate_swipe(device)
    simulate_swipe(device)
    
    time.sleep(random.uniform(0.3, 0.7))
    
    # Simulate touches along diamond perimeter
    simulate_perimeter_touches(device)



    
    return False

# Connect to device
device = connect_device()

# Continuous reading every 1.5 seconds


if device:
    while True:
        if (get_text_in_region_and_process(device, x1=95, y1=98, x2=225, y2=125) == True):
            attack(device)
        time.sleep(1.5)

"""
if device:
    while True:
        print(device.shell("wm size"))
        break
"""
