import requests

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

    def query(self,CountyName:str,TownName:str) -> tuple:
        print("query:",self.w[CountyName][TownName])
        return self.w[CountyName][TownName]