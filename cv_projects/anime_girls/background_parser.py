from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, shutil
import urllib.request

page = "https://lemmasoft.renai.us/forums/viewtopic.php?f=52&t=17302"
link_xpath = "//a[@class = 'postlink']"
output_path = "./cv_projects/anime_girls/backgrounds/"
if not os.path.exists(output_path):
    os.makedirs(output_path)
else:
    shutil.rmtree(output_path)
    os.makedirs(output_path)


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options = chrome_options)
driver.get(page)
element_list = driver.find_elements(By.XPATH, (link_xpath))
href_list = [elm.get_attribute("href") for elm in element_list]
for num, href in enumerate(href_list):
    urllib.request.urlretrieve(href, output_path+ "bck_" + str(num) + ".jpg")
driver.close()
