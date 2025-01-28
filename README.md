# Hand-Control
Software to perform actions based in hand gesture, using Yolo and RGB Camera.

# Setup steps
1- Create a python venv in the folder you'll throw this project then activate the venv:
 ' python -m venv venv ' -> ' venv\Scripts\Activate '

2- Section of pip install:
 ' pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 '
 ' pip install ultralytics '
 ' pip install pyautogui ' 
 ' pip install pyyaml '

3- download Hagrid yolov10x_gesture.pt model from https://github.com/hukenovs/hagrid and throw inside of the project folder.

4- run the main.py script

5- edit the gesture_config file to your liking.
 ( by default, this code is made to work with pyautogui, so use it as a base to see which actions or keys are valid. )

6- This is a side project that i'll work on every now and then, so far the software is missing an UI, options about showing the camera or not, and a few other things.

Credits:

Pre-trained Yolov10 model for hand gesture by : https://github.com/hukenovs/hagrid
