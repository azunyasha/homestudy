from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
import time


page = "https://ru.pinterest.com/pin/309552174392744341/"

#importing the necessary libraries
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options = chrome_options)

img_src = []
for i in range(50):
    driver.get(page)
    time.sleep(5)
    old_height = 0


    link_xpath = "//a[@class='Wk9 CCY S9z ho- kVc xQ4 iyn']"
    element = driver.find_elements(By.XPATH, (link_xpath))
    page = element[2].get_attribute("href")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        img_elements = driver.find_elements(By.CSS_SELECTOR,("img"))
        try:
            img_src += [elem.get_attribute('src') for elem in img_elements]
        except:
            pass
        if old_height == new_height:
            break
        old_height = new_height

img_src = list(dict.fromkeys(img_src))
driver.close()
output_str = ""
for src in img_src:
    output_str += src
    output_str += "\n"
with open('./cv_projects/anime_girls/href_list.txt', 'w') as output_file:
    output_file.write(output_str)
    output_file.close()
