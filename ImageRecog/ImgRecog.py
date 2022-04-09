import cv2
import numpy as np


img_fl=r"TrainImgs\Previous train image\aa688a20-15a7-4677-b6af-e99fbf8acef0.jpg"
class_file=r"TrainImgs\cascade\cascade.xml"

img=cv2.imread(img_fl)

b_n_w=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

car_track=cv2.CascadeClassifier(class_file)

cars=car_track.detectMultiScale(b_n_w)

for (x,y,w,h) in cars:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)


cv2.imshow("Name", img)

cv2.waitKey()

print("yes")


#https://www.analyticsvidhya.com/blog/2020/04/vehicle-detection-opencv-python/