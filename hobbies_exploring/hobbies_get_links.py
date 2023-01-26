from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

homepage = 'https://en.wikipedia.org/wiki/List_of_hobbies'


driver = webdriver.Chrome()
driver.get(homepage)
content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
driver.close()

paragraphs = soup.find_all("div", {'class' : 'div-col' })
table = []
for par in paragraphs:
    for hobb in par.find_all("a"):
        table += [{
            'name': hobb.get('title'),
            'link': hobb.get('href')
        }]

frame = pd.DataFrame(table)
frame = frame.dropna()
frame = frame.sort_values(by=['name'])
frame.to_excel('hobbies.xlsx')
