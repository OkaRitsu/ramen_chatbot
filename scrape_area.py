from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import time

new_ramen_store = pd.read_csv("./data/100_ramen_store.csv")
for i, url in enumerate(new_ramen_store["url"]):
    res = request.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser')
    area = soup.find_all(class_='listlink')
    print(area[1].get_text())
    new_ramen_store.loc[i, "area"] = area[1].get_text()
    time.sleep(1)


new_ramen_store.to_csv('./data/new_ramen_store.csv')
