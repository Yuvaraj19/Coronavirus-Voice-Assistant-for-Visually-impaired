import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_data():

    url="https://www.worldometers.info/coronavirus/"

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")
    table = soup.find("table", id = "main_table_countries_today")
    table_data = table.tbody.find_all("tr")

    dicts = {}
    for i in range(len(table_data)):
        try:
            key = (table_data[i].find_all('a', href=True)[0].string)
        except:
            key = (table_data[i].find_all('td')[0].string)

        value = [j.string for j in table_data[i].find_all('td')]
        dicts[key] = value

    live_data= pd.DataFrame(dicts).drop(0).T.iloc[:,:8]
    live_data.columns = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered","Active","Serious Critical"]
    live_data.index.name = 'Country'
    
    live_data.iloc[:,[1,3,5]].to_csv("Corona_data_new.csv")

get_data()
