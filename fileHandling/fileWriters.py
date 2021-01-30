import os
import sys
import zipfile

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