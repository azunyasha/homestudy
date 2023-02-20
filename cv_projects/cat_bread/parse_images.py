from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request



import json
import time
import os

#return array with all image src from search result
def stock_img_src(driver, link, num_max):
    img_src = []
    for i in range(2250, num_max, 150):
        print(link + "?start=" + str(i))
        img_src += page_img_src(driver, link + "?start=" + str(i))
    return img_src

#return array with all image src on the page
def page_img_src(driver, link):
    driver.get(link)
    img_elements = driver.find_elements(By.CSS_SELECTOR, ("img"))
    img_src = [elem.get_attribute('src') for elem in img_elements]
    return img_src

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
        if os.path.isfile(file):
            #print('Deleting file:', file)
            os.remove(file)
    link = links[key]
    img_src = stock_img_src(driver, link, 6000)
    filenum = 0
    for img in img_src:
        if img is not None:
            filename = project_path + key + "/" + str(filenum) + ".jpg"
            urllib.request.urlretrieve(img, filename)
            filenum += 1

driver.close()
print("success")
