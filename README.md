## Requirements

Before running the executable, ensure the following are set up on your Windows machine:

### 1. **Install ADB (Android Debug Bridge)**

The executable requires ADB to interact with an Android device. You need to install ADB manually and ensure that your device is connected and recognized by the system.

#### Steps to Install ADB:

1. Download the **ADB platform tools** for Windows from [here](https://developer.android.com/studio#command-tools).
2. Extract the downloaded file to a directory of your choice (e.g., `C:\adb`).
3. Add the ADB directory to your system's **Environment Variables**:
   - Right-click on `This PC` and select `Properties`.
   - Click on `Advanced system settings` > `Environment Variables`.
   - Under `System variables`, find and select `Path`, then click `Edit`.
   - Click `New` and add the directory where you extracted the ADB tools (e.g., `C:\adb`).
4. Open a new command prompt and type `adb version` to verify that ADB is installed correctly.

### 2. **Set Up Android Device**

1. Enable **Developer Options** on your Android device:
   - Go to `Settings` > `About Phone` and tap `Build Number` multiple times until it says you are a developer.
2. Enable **USB Debugging** in Developer Options:
   - Go to `Settings` > `Developer Options` and enable `USB Debugging`.
3. Connect your Android device to your PC via USB cable.

## 3. **Running the Executable**
Once you have set up ADB and connected your device:

Launch the Executable:

Double-click the .exe file to launch the bot.
The bot will automatically connect to your Android device via ADB and perform the programmed actions.
You should see output in the console indicating the bot is running.
Interact with the Bot: The bot will continuously monitor your Android device and perform actions based on the values detected on the screen.

##4. **Changing the code**
If you want to change the code, go ahead, its written in python 3.12
the requirements are in the txt file, email ankeetprasai@gmail.com and ill try to answer questions!
