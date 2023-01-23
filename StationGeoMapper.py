# 역 주소 -> 위도, 경도 매핑

import csv
import os
import json
from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')

ROOT = 'static'
DIR_NAME = '지하철역'
STATIC_FILE_PATH = os.path.join(ROOT, DIR_NAME)

# 도로명주소/지번주소를 위도 경도로 변환
def convertGeo(address):
    try:
        geo = geo_local.geocode(address)
        lat_lon = [geo.latitude, geo.longitude]
        return lat_lon
    except:
        return [0, 0]

# 이미 위도&경도 값이 있는 json 파일을 읽어옴
def setStationCoordinate():
    result = {}
    with open(os.path.join(ROOT, 'station_coordinate.json'), 'r', encoding='utf8') as f:
        stationCoordinateList = json.load(f)
        for station in stationCoordinateList:
            result[station['name']] = station
    return result


successList = []
failList = []
stationCoordinateDict = setStationCoordinate()


for filename in os.listdir(STATIC_FILE_PATH):
    print('{} CONVERTING...'.format(filename))
    with open(os.path.join(STATIC_FILE_PATH, filename), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line_nubmer, name, road_address, lot_number_address = row[
                '선명'], row['역명'], row['도로명주소'], row['지번주소']
            lat, lon = convertGeo(lot_number_address)
            if [lat, lon] == [0, 0]:
                lat, lon = convertGeo(row['도로명주소'])
            if [lat, lon] == [0, 0]:
                try:
                    stationMeta = {}
                    if name in stationCoordinateDict:
                        stationMeta = stationCoordinateDict[name]
                    elif name.split('(')[0] in stationCoordinateDict:
                        stationMeta = stationCoordinateDict[name.split('(')[0]]
                    lat, lon = stationMeta['lat'], stationMeta['lng']
                except:
                    print('[ERROR] {}'.format(name))
                    pass
            station = {
                'lineNumber': line_nubmer,
                'name': name,
                'lotNumberAddress': lot_number_address,
                'roadName': road_address,
                'lat': lat,
                'lon': lon
            }
            if [lat, lon] == [0, 0]:
                failList.append(station)
            else:
                successList.append(station)
    print('{} DONE!'.format(filename))

RESULT_PATH = 'results'
SUCCESS_FILE_NAME = 'success.json'
FAIL_FILE_NAME = 'fail.json'
with open(os.path.join(RESULT_PATH, SUCCESS_FILE_NAME), 'w', encoding='utf8') as outfile:
    json.dump(successList, outfile, ensure_ascii=False, indent='\t')
with open(os.path.join(RESULT_PATH, FAIL_FILE_NAME), 'w', encoding='utf8') as outfile:
    json.dump(failList, outfile, ensure_ascii=False, indent='\t')
