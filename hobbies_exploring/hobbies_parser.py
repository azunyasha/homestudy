from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import string

def get_soup(page):
    driver = webdriver.Chrome()
    driver.get(page)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    driver.close()
    return soup

def parse_page(page):
    homepage = 'https://en.wikipedia.org'
    soup = get_soup(homepage+page)
    paragraphs = soup.find_all("p")
    return ''.join([par.text for par in paragraphs])

homepage = 'https://en.wikipedia.org/wiki/List_of_hobbies'

soup = get_soup(homepage)
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
frame = frame.head()
frame['text'] = frame.link.apply(lambda x: parse_page(x))
frame['text_clean'] = frame.text.apply(
    lambda x: x.translate(str.maketrans('','', string.punctuation)).lower()
)
frame.to_excel('hobbies.xlsx')
