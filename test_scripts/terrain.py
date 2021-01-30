# import requests
# import urllib3

import urllib3
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import navpy 
import os
import string
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from fileHandling.fileWriters import *
from terrainGen.generateTerrain import *

        
def main():
    
    try:
    
        
        # Get cwd
        setdir = os.getcwd()
        
        # Command line input
        model_name = "cedar_point"
        file_path = model_name
        height_img_name = model_name+"_heightmap"
        aerial_img_name = model_name+"_aerial"

        size_m = 400
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if not os.path.exists(file_path+"/textures"):
            os.mkdir(file_path+"/textures")

        max_alt = gen_terrain( file_path, height_img_name, aerial_img_name, 29.65940870158524, -94.92315354313708, size_m )
        

        # Change to templates directory
        os.chdir("../templates")
        
        # Read template files
        config_template = read_template("config_temp.txt")
        sdf_template = read_template("sdf_temp.txt")
        
        # Change to model directory
        os.chdir(setdir+"/"+file_path)
        
        # Write to model.config
        write_config_file(config_template, model_name, "auto-gne", "na", "auto-gened by intelligent quads")        
        
        # Write to model.sdf
        write_sdf_file(model_name, height_img_name, aerial_img_name, sdf_template, size_m, size_m, max_alt )
        
    finally:
        
        # Change back to cwd
        os.chdir(setdir)

main()