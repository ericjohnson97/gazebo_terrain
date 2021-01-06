#!/usr/bin/env python
# Copyright 2017 University of Cincinnati
# All rights reserved. See LICENSE file at:
# https://github.com/MatthewVerbryke/gazebo_terrain
# Additional copyright may be held by others, as reflected in the commit history.


import os
import string
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from fileHandling.fileWriters import *    
        
def main():
    
    try:
        
        # Get cwd
        setdir = os.getcwd()
        
        # Command line input
        file_path = "colorado"
        height_img_name = "coloradoheightmap"
        aerial_img_name = "aerial"
        model_name = "colorado"
        # Change to templates directory
        os.chdir("../templates")
        
        # Read template files
        config_template = read_template("config_temp.txt")
        sdf_template = read_template("sdf_temp.txt")
        
        # Change to model directory
        os.chdir(setdir+"/../example_models/"+file_path)
        
        # Write to model.config
        write_config_file(config_template, model_name, "auto-gne", "na", "auto-gened by intelligent quads")        
        
        # Write to model.sdf
        write_sdf_file(model_name, height_img_name, aerial_img_name, sdf_template, 400, 400, 69 )
        
    finally:
        
        # Change back to cwd
        os.chdir(setdir)

        
main()        
        