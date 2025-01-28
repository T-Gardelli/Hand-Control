import cv2
from ultralytics import YOLO
import pyautogui
import time
import yaml

# Load the gesture configuration from YAML file
try:
    with open("gesture_config.yml", "r") as config_file:
        gesture_config = yaml.safe_load(config_file)
except FileNotFoundError:
    print("Error: gesture_config.yml not found!")
    exit(1)
except yaml.YAMLError:
    print("Error: Invalid YAML format in gesture_config.yml")
    exit(1)

# Initialize variables for cooldown periods
last_pressed = {}

# Load the model (hand gesture model)
model = YOLO('YOLOv10x_gestures.pt')

# Initialize the video capture device (webcam)
cap = cv2.VideoCapture(0)

while True:
    # Read each frame from the webcam every 200ms
    ret, frame = cap.read()
    
    # Perform inference on the current frame
    results = model(frame)
    
    # Check for any detected hand gestures
    if len(results[0].boxes) > 0:
        boxes = results[0].boxes
        labels = [model.model.names[int(box.cls)] for box in boxes]
        
        # Process each detected gesture
        for label in labels:
            if label in gesture_config:
                gesture = gesture_config[label]
                
                current_time = time.time()
                
                # Check cooldown period
                if label not in last_pressed or current_time - last_pressed[label] >= gesture.get('cooldown', 0):
                    # Execute the action based on configuration
                    if gesture['action'] == 'exit':
                        print("Holy gesture detected! - Stopping script")
                        cap.release()
                        cv2.destroyAllWindows()
                        exit(0)
                    elif gesture['action'] == 'key_press':
                        key = gesture.get('key', '')
                        if key:
                            print(f"Gesture '{label}' detected - Pressing {key}")
                            pyautogui.press(key)
                            last_pressed[label] = current_time
                    elif gesture['action'] == 'scroll':
                        scroll_amount = gesture.get('amount', 0)
                        direction = gesture.get('direction', 'down')
                        if scroll_amount != 0:
                        # Determine the correct sign for scrolling based on direction
                            if direction == 'up':
                                scroll_multiplier = -25
                            else:
                                scroll_multiplier = 25
                            print(f"Gesture '{label}' detected - Scrolling {direction}")
                            pyautogui.scroll(scroll_amount * scroll_multiplier)
                            last_pressed[label] = current_time
        
        # Draw bounding boxes around the detected hands (optional)
        annotated_frame = results[0].plot()
        cv2.imshow('Hand Detection', annotated_frame)
    else:
        # No hand detected, show original frame
        cv2.imshow('Hand Detection', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break  # Exit loop when 'q' is pressed

# Release the video capture device and close all windows
cap.release()
cv2.destroyAllWindows()

print("Hand detection script terminated.")