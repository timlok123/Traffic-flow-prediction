# -*- coding: utf-8 -*-
# Import module 
from bs4 import BeautifulSoup 
import requests 
import time
import os

# Get page content 
url = "https://static.data.gov.hk/td/traffic-snapshot-images/code/Traffic_Camera_Locations_En.xml"

def scrape_picture_function(number):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")

  #load the data and pack them in tuple 
  url_tags = soup.find_all("url")
  place_tags = soup.find_all("description")

  place_url_list = []

  for i in range(len(url_tags)):
    temp_url = (str(url_tags[i]).replace("<url>","")).replace("</url>","")
    temp_place = ((str(place_tags[i]).replace("<description>","")).replace("</description>","")).replace(" ","_")
    place_url_list.append((temp_place,temp_url))
  
  # Download the image and store it somewhere

  for count, i in enumerate(place_url_list):
    # It is too time consuming to download all 940 data, so I just download the first 10 first 
    # Adjust by the parameters of this funtion
    if count>=number:
      break

    image_url = str(i[1])
    t = time.localtime()
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S",t)
    folder_name ="Import_code _and_image_store\ "+str(i[0])
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    name_of_image = '{}\Index{count}_{place}_{time}.jpg'.format(folder_name,count=count, place=str(i[0]),time=current_time)
    try:

      with open(name_of_image, 'wb') as f:
        f.write(requests.get(image_url).content)
        f.close()
    except:
      print("Index_{no} images goes wrong".format(no=count))
  
  print("Import complete")

#Can change how many data you want to load 
scrape_picture_function(number=10)
