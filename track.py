from collections import defaultdict
from ultralytics import YOLO
import cv2
import math
import numpy as np
import os
import time
import requests

#calculate angle between two points
def get_angle(dot1, dot2):
    dot1 = np.array(dot1)
    dot2 = np.array(dot2)
    vector = dot2 - dot1
    angle_rad = np.arctan2(vector[1], vector[0])
    angle_deg = np.degrees(angle_rad)
    return float(angle_deg)

blue_dot_coordinates = [0.0,0.0]
yel_dot_coordinates = [0.0,0.0]


# Loading model
model = YOLO(r'C:\Users\karag\Documents\SeniorDesignProject\Ultralytics\runs\detect\train4\weights\best.pt')
model.to('cuda')  # Move model onto GPU
vid = cv2.VideoCapture(0)

# Perform tracking with the model
while vid.isOpened():
    success, frame = vid.read()
    if success:
        height, _ = frame.shape[:2]
        results = model.track(frame, show=True, persist=True, verbose=False)  # Tracking with default tracker

        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            for box in boxes:
                # Get the center of the box tensor
                x_center = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
                y_center = height - ((box.xyxy[0][1] + box.xyxy[0][3]) / 2)

                # Convert tensor to numerical values
                x_center_value = x_center.item()
                y_center_value = y_center.item()

                cls = box.cls     # Class index
                cls_int = int(cls)  #Class index as integer
                label = model.names.get(cls_int)    # .names is a integer indexed dictionary of classes
                conf = box.conf.item()     # Confidence score
                
                # desicion based on label, update spesific position variable
                if label == "Blue Dot":
                    blue_dot_coordinates = [x_center_value, y_center_value]
                elif label == "Yellow Dot":
                    yel_dot_coordinates = [x_center_value, y_center_value]
                else: 
                    print("Error in assigning coordinates")
                car_angle = get_angle(yel_dot_coordinates, blue_dot_coordinates)
                url = "http://localhost:8080/angles/" #site to post angles to
                data = {"car_angle": car_angle}
                try:
                    response = requests.post(url, json=data)
                    response.raise_for_status()
                    print("Anlge sent correctly")
                except Exception as e:
                    print("failed to send: ", e)
                print(car_angle)
        
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    else:
        pass

vid.release()
cv2.destroyAllWindows()