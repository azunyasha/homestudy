import pandas as pd
import http
from selenium import webdriver

homepage = 'https://www.gismeteo.ru/diary/4368/'

def get_weather_frame(year, month):
    driver = webdriver.Chrome()
    driver.get(homepage+str(year)+'/'+str(month))
    content = driver.page_source
    data = pd.read_html(content)
    data = pd.concat([data[0]['День','Температура'],data[0]['Число','Число']], axis = 1)
    data['Месяц'] = month
    data['Год'] = year
    data = pd.DataFrame(data.values)
    data.columns = ['Temperature','Day','Month','Year']
    return data


frames = []
try:
    for year in range(1998, 2023):
        for month in range(1,13):
            frames += [get_weather_frame(year,month)]
except:
    data = pd.concat(frames)
data = pd.concat(frames)
data.to_excel('weather.xlsx')
