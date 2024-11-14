from ppadb.client import Client as AdbClient

# Initialize ADB connection
def connect_device():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if len(devices) == 0:
        print("No device connected.")
        return None
    print("Device connected.")
    return devices[0]

# Simulate touch
def simulate_touch(device, x, y):
    if device:
        command = f"input tap {x} {y}"
        device.shell(command)
        print(f"Simulated touch at ({x}, {y}).")

# Connect to device and simulate touch
device = connect_device()
if device:
    simulate_touch(device, x=1460, y=525)  # Replace 500, 500 with your desired coordinates
