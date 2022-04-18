import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

col_list = []
pist_list = []
date_list = []
winner_list = []
car_list = []
laps_list = []
time_list = []

session = HTMLSession()
url = "https://www.formula1.com/en/results.html/"
page_list = ["races", "drivers", "team", "fastest-laps"]
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


def get_page_contents(base_url, paging_extra, pistList, dateList, winnerList, carList, lapsList, timeList):
    url = base_url + paging_extra
    r = session.get(url)
    source = BeautifulSoup(r.content, "lxml")  # Extracting the content of the requested page
    col = source.find("thead").find_all("th")
    for name in col:
        if name.text != "":
            col_list.append(name.text)
    prix_list = source.find("tbody").find_all("a", attrs={"class": "dark bold ArchiveLink"})
    for prix in prix_list:
        pistList.append(prix.text.strip())

    dates = source.find_all("td", attrs={"class": "dark hide-for-mobile"})
    for date in dates:
        dateList.append(date.text.strip())

    names = source.find_all("span", attrs={"class": "hide-for-tablet"})
    surnames = source.find_all("span", attrs={"class": "hide-for-mobile"})
    for i in range(len(names)):
        name = names[i]
        surname = surnames[i]
        winnerList.append((name.text + surname.text).strip())

    cars = source.find_all("td", attrs={"class":"semi-bold uppercase"})
    for car in cars:
        carList.append(car.text.strip())

    laps = source.find_all("td", attrs={"class": "bold hide-for-mobile"})
    for lap in laps:
        lapsList.append(lap.text.strip())

    times=source.find_all("td", attrs={"class": "dark bold hide-for-tablet"})
    for time in times:
        timeList.append(time.text.strip())

try:
    for i in range(1950, 2023):
        paging_extra = str(i) + "/races.html"
        get_page_contents(url, paging_extra, pist_list, date_list, winner_list, car_list, laps_list, time_list)
    col_list = np.unique(col_list)
    df = pd.DataFrame(columns=col_list)
    df['Grand Prix'] = pist_list
    df['Date']=date_list
    df['Winner'] = winner_list
    df['Car']=car_list
    df['Laps']=laps_list
    df['Time']=time_list

    df.to_csv("./output/races.csv")
    print(df)
except Exception as e:
    print("Bir sıkıntı vağğğğğğ")
