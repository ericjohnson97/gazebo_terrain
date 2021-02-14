import urllib3
import requests
import json
import numpy as np
import cv2
import navpy
import os
import string
import sys


def gen_terrain(path, height_img_name, aerial_img_name, lat_ref, lon_ref, size_m):
    ned_sw = [-size_m/2, -size_m/2, 0]
    ned_ne = [size_m/2, size_m/2, 0]
    print("ne", ned_ne)
    alt_ref = 0

    lla_sw = navpy.ned2lla(ned_sw, lat_ref, lon_ref, alt_ref,
                           latlon_unit='deg', alt_unit='m', model='wgs84')
    print(lla_sw)

    lla_ne = navpy.ned2lla(ned_ne, lat_ref, lon_ref, alt_ref,
                           latlon_unit='deg', alt_unit='m', model='wgs84')
    print(lla_ne)

    bbox = str(lla_sw[0])+","+str(lla_sw[1])+"," + \
        str(lla_ne[0])+","+str(lla_ne[1])
    print(bbox)

    http = urllib3.PoolManager()

    res = 17
    # url = 'http://www.thefamouspeople.com/singers.php'
    url = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds?bounds=39.45312178126139,-105.66816658410795,39.475187097556585,-105.64420457918649&rows=10&cols=10&heights=sealevel&key=Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh"
    response = http.request('GET', url)

    url = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds"
    payload = {'bounds': bbox,
               'rows': str(res), 'cols': str(res), 'heights': 'sealevel', 'key': 'Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh'}
    resp = requests.get(url, params=payload)
    data = json.loads(resp.text)

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
            picarray[ycord][col] = np.uint8(
                (array[counter] - minnum)/(maxnum-minnum) * 255)
            counter = counter + 1

    cv2.imwrite(path+'/textures/'+height_img_name+'.png', picarray)
    img = cv2.imread(path+'/textures/'+height_img_name+'.png')
    dim = (1025, 1025)
    im_big = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    blur = cv2.GaussianBlur(im_big, (501, 501), 0)
    blur90 = cv2.rotate(blur, cv2.cv2.ROTATE_90_CLOCKWISE) 
    cv2.imwrite(path+'/textures/'+height_img_name+'.png', blur90)

    max_alt = maxnum-minnum
    print('height diff', max_alt)

    aerial_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial"

    aerial_payload = {'mapArea': bbox, 'mapSize': '1025,1025', 'fmt': 'png',
                      'key': 'Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh'}
    resp = requests.get(aerial_url, params=aerial_payload)

    with open(path+"/textures/"+aerial_img_name+".png", 'wb') as f:
        f.write(resp.content)

    aerial_img = cv2.imread(path+"/textures/"+aerial_img_name+".png")
    aerial90 = cv2.rotate(aerial_img, cv2.cv2.ROTATE_90_CLOCKWISE) 
    aerial90 = cv2.convertScaleAbs(aerial90, alpha=1.5, beta=0)
    cv2.imwrite(path+"/textures/"+aerial_img_name+".png", aerial90)
    print(aerial_url)

    return max_alt