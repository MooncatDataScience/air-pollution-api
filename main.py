import requests
import csv
import time

def get_aqi_data():
    url = ''
    data = requests.get(url)
    data_json = data.json()
    
    aqi_data = []
    for i in data_json['records']:
        if i['county'] == '臺中市':
            row = {
                'site': i['sitename'],
                'county': i['county'],
                'pollutant': i['pollutant'],
                'so2': i['so2'],
                'co': i['co'],
                'o3':i['o3'],
                'o3_8hr': i['o3_8hr'],
                'pm10': i['pm10'],
                'pm2.5': i['pm2.5'],
                'no2': i['no2'],
                'nox': i['nox'],
                'no': i['no'],
                'wind_speed': i['wind_speed'],
                'wind_direc': i['wind_direc'],
                'publishtime': i['publishtime'],
                'co_8hr': i['co_8hr'],
                'pm2.5_avg': i['pm2.5_avg'],
                'pm10_avg': i['pm10_avg'],
                'so2_avg': i['so2_avg'],
                'longitude': i['longitude'],
                'latitude': i['latitude'],
                'aqi': i['aqi'],
                'status': i['status'],
            }
            aqi_data.append(row)
    
    return aqi_data

while True:
    aqi_data = get_aqi_data()
    
    with open('aqi_data.csv', mode='a', newline='') as csvfile:
        fieldnames = ['site', 'county', 'pollutant', 'so2', 'co','o3','o3_8hr', 'pm10', 'pm2.5', 'no2', 'nox', 'no'
, 'wind_speed', 'wind_direc', 'publishtime', 'co_8hr', 'pm2.5_avg', 'pm10_avg', 'so2_avg', 'longitude', 'latitude', 'aqi', 'status',]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        for row in aqi_data:
            writer.writerow(row)
    
    now = time.ctime()
    print("寫入成功", now)
    
    time.sleep(3600) # 暫停 3600 秒，也就是 1 小時
