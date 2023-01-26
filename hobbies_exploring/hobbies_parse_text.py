from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
def parse_par(page):
    driver = webdriver.Chrome()
    homepage = 'https://en.wikipedia.org'
    driver.get(homepage+page)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    driver.close()
    pars = soup.find_all("p")
    return [par.text for par in pars]

data = pd.read_excel('sexes.xlsx')

data['text'] = data.link.apply(lambda x: parse_par(x))
data.to_excel('hobbies.xlsx')
