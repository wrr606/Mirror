import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class News:
    def __init__(self):
        url="https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant"
        res = requests.get(url)
        temp = BeautifulSoup(res.text)
        temp=temp.find("c-wiz",class_="D9SJMe").find_all("c-wiz",class_="PO9Zff Ccj79 kUVvS")
        self.news=[]
        for i in temp:
            for j in i.find_all("div",class_="f9uzM"):
                href=urljoin("https://news.google.com", j.find('a', class_='WwrzSb')['href'])
                self.news.append([j.find('a', class_="gPFEn").text,href])

x=News()
print(x.news[0][1])

class Weather:
    def __init__(self):
        url="https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=CWA-7F582D1E-0E78-4FF7-9EDF-651C4B30A197&downloadType=WEB&format=JSON"
        data=requests.get(url).json()
        location=data['cwaopendata']['dataset']["Station"]
        self.w={}
        for i in location:
            city=i["GeoInfo"]['CountyName']# 縣市
            area=i["GeoInfo"]['TownName']# 鄉鎮
            temp=i["WeatherElement"]["AirTemperature"] #溫度
            state=i["WeatherElement"]["Weather"] #狀態
            if city in self.w:
                if area not in self.w[city]:
                    self.w[city][area]=(temp,state)
            else:
                self.w[city]={area:(temp,state)}
    
    #傳入縣市名和鄉鎮名，會回傳一個陣列，為 [溫度,當前天氣狀態]
    def query(self,CountyName:str,TownName:str) -> tuple:
        print("query:",self.w[CountyName][TownName])
        return self.w[CountyName][TownName]
    
    #更新當前資料
    def update(self):
        url="https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=CWA-7F582D1E-0E78-4FF7-9EDF-651C4B30A197&downloadType=WEB&format=JSON"
        data=requests.get(url).json()
        location=data['cwaopendata']['dataset']["Station"]
        self.w={}
        for i in location:
            city=i["GeoInfo"]['CountyName']# 縣市
            area=i["GeoInfo"]['TownName']# 鄉鎮
            temp=i["WeatherElement"]["AirTemperature"] #溫度
            state=i["WeatherElement"]["Weather"] #狀態
            if city in self.w:
                if area not in self.w[city]:
                    self.w[city][area]=(temp,state)
            else:
                self.w[city]={area:(temp,state)}

"""
使用方法

from Crawler import News,Weather

創建一個物件 x=Weather()

使用查詢功能 x.query()

更新當前天氣 x.update()

創建一個新聞爬蟲物件 x=News()

全部新聞 x.news

x.news[i][0] 第 i 篇新聞的標題

x.news[i][1] 第 i 篇新聞的網址
"""