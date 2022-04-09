# Import module 
from bs4 import BeautifulSoup 
import requests 
import time
import os

def fetch_image(Required_tags):
# Get page content 
  url = "https://static.data.gov.hk/td/traffic-snapshot-images/code/Traffic_Camera_Locations_En.xml"

  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")

  #load the data and pack them in tuple 
  url_tags = soup.find_all("url")
  place_tags = soup.find_all("description")
  key_tags = soup.find_all("key")

  place_url_key_list = []

  for i in range(len(url_tags)):
    temp_url = (str(url_tags[i]).replace("<url>","")).replace("</url>","")
    temp_place = ((str(place_tags[i]).replace("<description>","")).replace("</description>","")).replace(" ","_")
    temp_key = ((str(key_tags[i]).replace("<key>","")).replace("</key>",""))
    if str(temp_key) in Required_tags:
      place_url_key_list.append((temp_place,temp_url))
  
  return place_url_key_list

def scrape_picture_function(place_url_key_list):

  # Download the image and store it somewhere
  for count, i in enumerate(place_url_key_list):

    current_place = str(i[0])
    current_place_folder_name = current_place.split("_")[-1]
    image_url = str(i[1])
    t = time.localtime()
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S",t)
    name_of_image = 'Index{count}_{place}_{time}.jpg'.format(count=count, place=current_place,time=current_time)

    #make a new directory and store it inside
    
    try:
      os.mkdir(os.path.join(os.getcwd(),current_place_folder_name))
    except:
      pass
    go_back = os.getcwd()
    os.chdir(os.path.join(os.getcwd(),current_place_folder_name))
  
    try:
      with open(name_of_image, 'wb') as f:
        f.write(requests.get(image_url).content)
        f.close()
    except:
      print("Index_{no} images goes wrong".format(no=count))
    
    #Return to the main_directory(loaded_img)a
    os.chdir(go_back)
    
  print("Import completed")

#Can change how many data you want to load 
Required_tags = ["AID03211","AID03106","AID01111","AID01213","TDSIEC10001"]
list1 = fetch_image(Required_tags)
while True:
  scrape_picture_function(list1)
  time.sleep(120)