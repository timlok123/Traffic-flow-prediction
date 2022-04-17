import cv2
import numpy as np
import os
import csv

files=["[AID01213]","[AID03106]","[AID03211]","[TDSIEC10001]"]#["[AID01111]",
def ImgRecog(files):

    os.chdir(r"Import_code_and_image_store")

    

    p=1
    for i in files:
        
        for filename in os.listdir(i):
            fd=open(i+'.csv','a')
            img_fl = os.path.join(i,filename)
            
            #img_fl="Import_code_and_image_store\\"+i+"\\"+filename
            
            
            
            class_file="cascade.xml"
            
            

            img=cv2.imread(img_fl)
            ugly=cv2.imread("Index0_Hong_Chong_Road_near_The_Hong_Kong_Polytechnic_University_-_Northbound_(1)_[AID01111]_2022_04_10_21_29_18.jpg")
            if p==1:
                last=ugly
                p=-1
            try:
                if not(np.bitwise_xor(ugly,img).any()) or not(np.bitwise_xor(img,last).any()) or type(img)=="NoneType":
                    print("identical/bad img:",filename)
                    #continue
                else:
                    #try:
                    b_n_w=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                    car_track=cv2.CascadeClassifier(class_file)

                    cars=car_track.detectMultiScale(b_n_w)
                    fd.write("{},{}\n".format(filename[-23:-4],len(cars)))
                    #print(filename[-23:-4],len(cars))
                    #except:
                        #print(filename)

                
            except:
                print(filename)
            last=img
            fd.close()    

ImgRecog(files)  

#https://www.analyticsvidhya.com/blog/2020/04/vehicle-detection-opencv-python/