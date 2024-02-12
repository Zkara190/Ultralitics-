from collections import defaultdict
from ultralytics import YOLO
import cv2
import math
import numpy as np
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

blue_dot_coordinates = np.array([0,0])
yel_dot_coordinates = np.array([0,0])

#calculate the angle the car is pointing based on symbols
def car_angle(x_b,y_b,x_r,y_r):
    return math.degrees(math.atan((y_b-y_r)/(x_b-x_r)))

# calculate the direction vector 
def get_direction(p1,p2):
    return (p1 - p2)

# Loading model
model = YOLO(r'C:\Users\karag\Documents\SeniorDesignProject\Ultralytics\runs\detect\train4\weights\best.pt')
model.to('cuda')  # Move model onto GPU
vid = cv2.VideoCapture(0)

#set the driver to webdriver
driver = webdriver.Chrome()
#get the website
driver.get("http://192.168.137.123")

# Perform tracking with the model
while vid.isOpened():
    success, frame = vid.read()
    if success:

        results = model.track(frame, show=True, persist=True, verbose=False)  # Tracking with default tracker

        for result in results:
            
            boxes = result.boxes  # Boxes object for bbox outputs

            for box in boxes:
                # Get the center of the box tensor
                x_center = (box.xyxy[0][0] + box.xyxy[0][2]) / 2
                y_center = (box.xyxy[0][1] + box.xyxy[0][3]) / 2

                # Convert tensor to numerical values
                x_center_value = x_center.item()
                y_center_value = y_center.item()

                cls = box.cls     # Class index
                cls_int = int(cls)  #Class index as integer
                label = model.names.get(cls_int)    # .names is a integer indexed dictionary of classes
                conf = box.conf.item()     # Confidence score
                
                # desicion based on label, update spesific position variable
                if label == "Blue Dot":
                    blue_dot_coordinates[0] = x_center_value
                    blue_dot_coordinates[1] = y_center_value

                elif label == "Yellow Dot":
                    yel_dot_coordinates[0] = x_center_value
                    yel_dot_coordinates[1] = y_center_value
            
                else: 
                    print("Error in assigning coordinates")

                # list[0] = label
                # list[1] = conf.item()
                # list[2] = round(x_center_value,2)
                # list[3] = round(y_center_value,2)

                # print("Center coordinates X:", x_center_value, " Y:", y_center_value)
                # print("Class: ", label)
                # print("Confidence: ", conf)

    textbox = driver.find_element("name", "value")
    textbox.clear()
    textbox.send_keys("12")
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_button.click()
    time.sleep(1)
        
        #print("blue coordinates: ", blue_dot_coordinates)
        #print("yellow coordinates: ", yel_dot_coordinates)
        #print("vector: ", get_direction(blue_dot_coordinates, -(yel_dot_coordinates))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    else:
        pass

driver.quit()
vid.release()
cv2.destroyAllWindows()
