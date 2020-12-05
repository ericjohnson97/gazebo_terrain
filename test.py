import navpy 
ned_sw = [-200, -200, 0]
ned_ne = [ 200, 200, 0 ]
lat_ref = 39.5792921475838 
lon_ref = -105.94028071770592
alt_ref = 0


lla_sw = navpy.ned2lla(ned_sw, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')
print(lla_sw)

lla_ne = navpy.ned2lla(ned_ne, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')
print(lla_ne)

bbox = str(lla_sw[0])+","+str(lla_sw[1])+","+str(lla_ne[0])+","+str(lla_ne[1])
print(bbox)