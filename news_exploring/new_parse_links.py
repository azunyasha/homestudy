from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import time

class News_Parser:
    def __init__(self, sources = []):
        self.sources = sources

    def parse_main_page(
                  self, page, link_class,
                  switcher_tag = None,
                  next_button_tag = None
                 ):

        retry_num = 0
        while retry_num < 20:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options = chrome_options)
            try:
                driver.get(page)
                retry_num = 20
            except:
                driver.refresh()
                retry_num += 1
                print('reconnect', retry_num)

        if switcher_tag is not None:
            self.click_switcher(driver, switcher_tag)


        if next_button_tag is not None:
            for i in range(3):
                self.click_next_button(driver, next_button_tag)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        links = soup.find_all('a', {'class' : link_class})
        return [link.get('href') for link in links]

    #Метод для нажатия переключателя 'в хронологическом порядке'
    def click_switcher(self, driver, tag):
        switcher = driver.find_element(By.CLASS_NAME, tag)
        driver.execute_script("arguments[0].click();", switcher);
        print("pressing switcher")
        time.sleep(2)

    #Метод для нажатия конпки 'загрузить еще'
    def click_next_button(self, driver, tag):
        button = driver.find_element(By.CSS_SELECTOR, tag)
        driver.execute_script("arguments[0].click();", button);
        print('pressing button "next"')
        time.sleep(5)


news_parser = News_Parser()
sources = [
{
    'name' : 'meduza',
    'page' : 'https://meduza102.global.ssl.fastly.net',
    'homepage' : 'https://meduza102.global.ssl.fastly.net',
    'link_class' : 'ChronologyItem-link',
    'switcher_tag' : 'Switcher-module_control__1NTvY',
    'next_button_tag'  : '.Button-module_root__RpsiW.Button-module_default__28Vo_.Button-module_gold__ZMYg-'
},
{
    'name' : 'novaya_gazeta',
    'page' : 'https://novayagazeta.eu',
    'homepage' : 'https://novayagazeta.eu',
    'link_class' : 'E5d19 material-reference',
    'switcher_tag' : '_3a32F',
    'next_button_tag'  : '._1N-Xz'
},
{
    'name' : 'gazeta_ru',
    'page' : 'https://www.gazeta.ru/news',
    'homepage' : 'https://www.gazeta.ru',
    'link_class' : 'b_ear m_techlisting',
    'switcher_tag' : None,
    'next_button_tag'  : '.b_showmorebtn-link'
},
{
    'name' : 'kp',
    'page' : 'https://www.kp.ru/online',
    'homepage' : 'https://www.kp.ru',
    'link_class' : 'sc-1tputnk-2 boKspN',
    'switcher_tag' : None,
    'next_button_tag'  : '.sc-abxysl-0.cBSVMU'
},
{
    'name' : 'rt',
    'page' : 'https://russian.rt.com/news',
    'homepage' : 'https://russian.rt.com',
    'link_class' : 'link link_color',
    'switcher_tag' : None,
    'next_button_tag'  : '.button__item.button__item_listing'
}
]



links_frame = []
for source in sources:
    links = news_parser.parse_main_page(source['page'],
        link_class = source['link_class'],
        switcher_tag = source['switcher_tag'],
        next_button_tag = source['next_button_tag']
    )
    names = [source['name']]*len(links)
    homepage = [source['homepage']]*len(links)
    links_frame += list(zip(names,homepage,links))

for count in range(100):
    insider_link = 'https://theins.ru/news/' + str(259024-count)
    links_frame += [('insider', 'https://theins.ru/news', insider_link)]


links_frame = pd.DataFrame(links_frame, columns = ['source','homepage','link'])
links_frame = links_frame.drop_duplicates()
links_frame['full_link'] = links_frame['link']
links_frame.loc[~links_frame.link.str.contains('https'),'full_link'] = (
    links_frame.loc[~links_frame.link.str.contains('https'),
    ['homepage','link']].sum(axis = 1)
)
links_frame.to_csv('news_links.csv',index=False)
