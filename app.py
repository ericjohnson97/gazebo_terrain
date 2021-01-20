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
from fileHandling.fileWriters import *
from terrainGen.generateTerrain import *


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    json_data = request.get_json()
    print(json_data)

    try:

        # Get cwd
        setdir = os.getcwd()

        # Command line input
        model_name = json_data['model_name']
        file_path = "static/" + model_name
        height_img_name = model_name+"_heightmap"
        aerial_img_name = model_name+"_aerial"
        print(json_data['sideLength'])
        size_m = float(json_data['sideLength'])
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

        os.chdir(setdir+'/static')
        # zip directory
        zipf = zipfile.ZipFile(model_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(model_name, zipf)
        zipf.close()

        os.chdir(setdir)

    finally:

        # Change back to cwd
        os.chdir(setdir)
    print(setdir)

    send_from_directory(setdir+'/static', model_name+'.zip')
    # os.remove(setdir+'/static/'+model_name+'.zip')
    return json.dumps({'success': True, 'filename': model_name+'.zip'}), 200, {'ContentType': 'json'}

def zipdir(path, ziph):
    print("ziping")
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    app.run()
