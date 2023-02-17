from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request



import json
import time
import os

# reading the data from the file
project_path = './cv_projects/cat_bread/'
with open(project_path+'links_list.txt') as f:
    links = f.read()

links = json.loads(links)
img_links = {}
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options = chrome_options)
for key in links.keys():
    if not os.path.isdir(project_path+key):
        os.makedirs(project_path+key)
    for file_name in os.listdir(project_path + key):
    # construct full file path
        file = project_path + key + "/" + file_name
        #print(file)
        #print(os.path.isfile(file))
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)
    link = links[key]
    driver.get(link)
    bottom_flag = 0
    height = driver.execute_script("return document.body.scrollHeight")
    while 1-bottom_flag:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == height:
            bottom_flag = 1
        else:
            height = new_height
    img_elements = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
    img_src = [elem.get_attribute('src') for elem in img_elements]
    filenum = 0
    for img in img_src:
        if img is not None:
            filename = project_path + key + "/" + str(filenum) + ".jpg"
            urllib.request.urlretrieve(img, filename)
            filenum += 1

driver.close()
print("success")
