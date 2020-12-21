from flask import Flask, jsonify, render_template, request, make_response, send_from_directory
import json
import urllib3
import requests
import numpy as np
import cv2
import navpy
import os
import string
import sys
import zipfile

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/download', methods=['GET', 'POST'])
def download():
    json_data = request.get_json()
    setdir = os.getcwd()
    print(setdir, json_data)
    # return json.dumps({'success': True, 'filename': 'cedar_point2.zip'}), 200, {'ContentType': 'application/json'} json_data['filename']
    return send_from_directory('static', 'cedar_point2.zip', as_attachment=True)


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    json_data = request.get_json()
    print(json_data)

    try:

        # Get cwd
        setdir = os.getcwd()

        # Command line input
        model_name = "cedar_point2"
        file_path = "static/" + model_name
        height_img_name = model_name+"_heightmap"
        aerial_img_name = model_name+"_aerial"

        size_m = 400
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if not os.path.exists(file_path+"/textures"):
            os.mkdir(file_path+"/textures")

        max_alt = gen_terrain(file_path, height_img_name, aerial_img_name,
                              json_data['latitude'], json_data['longitude'], size_m)

        # Change to templates directory
        os.chdir("templates")

        # Read template files
        config_template = read_template("config_temp.txt")
        sdf_template = read_template("sdf_temp.txt")

        # Change to model directory
        os.chdir(setdir+"/"+file_path)

        # Write to model.config
        write_config_file(config_template, model_name, "auto-gne",
                          "na", "auto-gened by intelligent quads")

        # Write to model.sdf
        write_sdf_file(model_name, height_img_name, aerial_img_name,
                       sdf_template, size_m, size_m, max_alt)

        os.chdir(setdir)
        # zip directory
        zipf = zipfile.ZipFile('static/'+model_name +
                               '.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('static/cedar_point2/', zipf)
        zipf.close()

    finally:

        # Change back to cwd
        os.chdir(setdir)
    print(setdir)
    return json.dumps({'success': True, 'filename': 'cedar_point2.zip'}), 200, {'ContentType': 'application/json'}
    # return send_from_directory(setdir, 'cedar_point2.zip', as_attachment=True)


def gen_terrain(path, height_img_name, aerial_img_name, lat_ref, lon_ref, size_m):
    ned_sw = [-size_m/2, -size_m/2, 0]
    ned_ne = [size_m/2, size_m/2, 0]
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
    cv2.imwrite(path+'/textures/'+height_img_name+'.png', blur)

    max_alt = maxnum-minnum
    print('height diff', max_alt)

    aerial_url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial"

    aerial_payload = {'mapArea': bbox, 'mapSize': '1025,1025', 'fmt': 'png',
                      'key': 'Ajp1x3U32EpQ0c8rngCiIUjfJeFCvnFDlp9hefsG2DuaLP8317j5Vs1qECcAqzEh'}
    resp = requests.get(aerial_url, params=aerial_payload)

    with open(path+"/textures/"+aerial_img_name+".png", 'wb') as f:
        f.write(resp.content)

    print(aerial_url)

    return max_alt


def read_template(temp_file_name):

    try:

        # Open template
        temp_file = open(temp_file_name, "r")

        # Read template
        temp_hold_text = temp_file.read()
        template = str(temp_hold_text)

        return template

    finally:

        # Close template
        temp_file.close()


def write_config_file(config_template, model_name, creator_name, email, description):

    try:
        # Replace indicated values
        config_template = config_template.replace("$MODELNAME$", model_name)
        config_template = config_template.replace("$AUTHORNAME$", creator_name)
        config_template = config_template.replace("$EMAILADDRESS$", email)
        config_template = config_template.replace("$DESCRIPTION$", description)

        # Ensure results are a string
        config_content = str(config_template)

        # Open config file
        target = open("model.config", "w")

        # Write to config file
        target.write(config_content)

    finally:

        # Close file
        target.close()


def write_sdf_file(model_name, height_img_name, aerial_img_name, sdf_template, size_x, size_y, size_z):

    # Filling in content
    sdf_template = sdf_template.replace("$MODELNAME$", model_name)
    sdf_template = sdf_template.replace("$FILENAME$", height_img_name)
    sdf_template = sdf_template.replace("$AERIAL_FILENAME$", aerial_img_name)
    sdf_template = sdf_template.replace("$SIZEX$", str(size_x))
    sdf_template = sdf_template.replace("$SIZEY$", str(size_y))
    sdf_template = sdf_template.replace("$SIZEZ$", str(size_z))

    # Ensure results are a string
    sdf_content = str(sdf_template)

    # Open file
    target = open("model.sdf", "w")

    # Write to model.sdf
    target.write(sdf_content)

    # finally:

    # Close file
    target.close()


def zipdir(path, ziph):
    print("ziping")
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    app.run()
