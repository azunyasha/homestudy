from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time

homepage = "https://meduza102.global.ssl.fastly.net/"


driver = webdriver.Chrome()
driver.get(homepage)

#Распологаем в хронологическом порядке - кликаем нужную кнопку
switcher = driver.find_element(By.CLASS_NAME, 'Switcher-module_control__1NTvY')
driver.execute_script("arguments[0].click();", switcher);
time.sleep(2)


#Три раза нажимаем кнопку "Далее" для подгрузки ленты
for i in range(3):
    button = driver.find_element(By.CLASS_NAME, 'Chronology-control')
    button = button.find_element(By.XPATH, ".//button")
    driver.execute_script("arguments[0].click();", button);
    time.sleep(2)


content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
driver.close()

news_frame = pd.DataFrame({
    "Content" : soup.find_all('a', {'class' : 'ChronologyItem-link'})
})

news_frame['Link'] = news_frame.Content.apply(
    lambda x : x.get('href')
)
news_frame['Text'] = news_frame.Content.apply(
    lambda x : x.getText()
)

news_frame = news_frame.drop("Content", axis = 1)
news_frame.to_excel("news_exploring\meduza_links.xlsx")
