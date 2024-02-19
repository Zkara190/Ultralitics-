from fastapi import FastAPI, Request
from pydantic import BaseModel
import serial

app = FastAPI()

class AngleData(BaseModel):
    car_angle: float
    target_angle: float

stored_angles = {"car": []}     #, "target": []}

#arduino = serial.Serial('COMX', 9600) #replacing COMX with the chosen port; 9600 is baud rate

@app.post("/angles/")
async def store_angle(angle_data: AngleData, request: Request):
    payload = await request.json()
    print("Request Payload:", payload)

    car_angle = angle_data.car_angle
    #target_angle = angle_data.target_angle

    stored_angles["car"].append(car_angle)
    #stored_angles["target"].append(target_angle)
    #arduino.write(angle.encode())

    return {"message": "Angle stored"}

@app.get("/angles/")
async def get_angles():
    return{"car_angles": stored_angles["car"]}      #, "target_angles": stored_angles["target"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)