from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')

model.to('cuda') # move model onto GPU

if __name__ == '__main__': #added to enable multiprocessing

    # training model
    results = model.train(data=r'C:\Users\karag\Pictures\blue and yellow dots.v5i.yolov8/data.yaml', epochs = 300, imgsz = 640)
