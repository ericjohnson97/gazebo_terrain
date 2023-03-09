# Gazebo Terrain Generator Website 

![img](static/img/colorado.png)

The website allows you to position of a bounding box over an aerial map view of a location on earth. Upon clicking generate, the site will contact bing maps, ask for an aerial view of the selected area as well as an array of the elevation of the area. This is then used to generate a gazebo model using a heightmap. The website automatically scales the model to the correct units to be used in your simulation.


**Notice** This project is no longer in development. The website is still functional, but the code is not maintained. The code was written when I was new to python and because of this, the code is not very clean. 

## Dependencies 
This project utilizes a flask backend. the dependencies for the server can be installed by running the following.
```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```



## Running the website

To run the website you will need to get a free bing maps API key. please go to https://www.microsoft.com/en-us/maps/choose-your-bing-maps-api to get started. Follow the scribe below to generate a key.


https://scribehow.com/shared/Create_Bing_Maps_API_Key__hgDeWKEmTCCyFFbsVFyhAw

Once you have your key, you will need to create a file called `api.json` in the config directory of the project. This file should have the following

```
{
    "bing_maps_key": "YOUR_KEY_HERE"
}
```


Once you have your key, you can run the website by running the following command
```
python3 app.py
```

the site will be hosted on `localhost:5000`