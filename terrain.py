# import requests
# import urllib3

# url = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds?bounds=39.45312178126139,-105.66816658410795,39.475187097556585,-105.64420457918649&rows=10&cols=10&heights=sealevel&key=Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh"

# aerial imagery
# https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial?&mapArea=39.45312178126139,-105.66816658410795,39.475187097556585,-105.64420457918649&mapSize=80,80&fmt=png&key=Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh


from bs4 import BeautifulSoup
import urllib3
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
http = urllib3.PoolManager()

res = 30
# url = 'http://www.thefamouspeople.com/singers.php'
url = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds?bounds=39.45312178126139,-105.66816658410795,39.475187097556585,-105.64420457918649&rows=10&cols=10&heights=sealevel&key=Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh"
response = http.request('GET', url)
# data = response.data
# soup = BeautifulSoup(response.data.decode('json'))
# print(soup)
# print(response.json)

url = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds"
payload = {'bounds': '39.45312178126139,-105.66816658410795,39.475187097556585,-105.64420457918649',
           'rows': str(res), 'cols': str(res), 'heights': 'sealevel', 'key': 'Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh'}
resp = requests.get(url, params=payload)
data = json.loads(resp.text)
# print(resp.url)
# print(data)
# print('')
print(data['resourceSets'][0]['resources'][0]['elevations'])
array = np.array(data['resourceSets'][0]['resources'][0]['elevations'])
print('array length', len(array))

maxnum = max(array)
print('max num', maxnum)
minnum = min(array)
print('min num', minnum)

counter = 0
picarray = np.empty([res, res])
for row in range(0, res):
    ycord = res-1 - row
    # print(ycord)
    for col in range(0, res):
        # print(np.uint8((array[counter] - minnum)/maxnum * 255))
        picarray[ycord][col] = np.uint8(
            (array[counter] - minnum)/(maxnum-minnum) * 255)
        counter = counter + 1


cv2.imwrite('mypng.png', picarray)

# img = Image.fromarray(picarray, 'L')
# img.save('my.png')
