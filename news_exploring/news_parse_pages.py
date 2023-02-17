from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

links = pd.read_csv('news_text.csv')

source_class_dic = {
    'meduza' : 'GeneralMaterial-article',
    'novaya_gazeta' : '_1dlNZ selection-range-available',
    'gazeta_ru' : 'b_article-text',
    'kp' : 'sc-1wayp1z-0 sc-1wayp1z-5 kLiiYm jhipZw',
    'rt' : 'article article_article-page',
    'insider' : 'xzBG5'
}


def parse_page(driver, tag):
    try:
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        print(tag)
        page_text = soup.find('div', {'class' : tag})
        return page_text.get_text()
    except:
        return None

#links['text'] = ""

for i in range(links.shape[0]):
#for i in range(3):
    if links.loc[i, 'text'] is np.nan:
        link = links.loc[i, 'full_link']
        retry_num = 0
        while retry_num < 20:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options = chrome_options)
            try:
                driver.get(link)
            except:
                retry_num +=1
                driver.close()
                print(link,'reconnect', retry_num)
            else:
                retry_num = 20
                class_tag = source_class_dic[links.loc[i,'source']]
                links.loc[i, 'text'] = parse_page(driver, class_tag)
                driver.close()
        links.to_csv('news_text.csv',index=False)
