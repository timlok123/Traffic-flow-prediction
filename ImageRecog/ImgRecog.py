import cv2
import numpy as np


img_fl=r"ImageRecog\3e6eb244-605d-4389-b66b-cc4c10a9b46e.jpg"
class_file=r"ImageRecog\cars1.xml"

img=cv2.imread(img_fl)

b_n_w=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

car_track=cv2.CascadeClassifier(class_file)

cars=car_track.detectMultiScale(b_n_w)

for (x,y,w,h) in cars:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)


cv2.imshow("Name", img)

cv2.waitKey()

print("yes")
