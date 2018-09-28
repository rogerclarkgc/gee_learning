# Metadata of image are stored as dict object
# image.getInfo() is a useful method to fetch source data from earthengine host

import ee
from pprint import pprint

ee.Initialize()

# Load an image
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Get information about the bands as a list
bandNames = image.bandNames()
pprint(bandNames.getInfo())

# Get projection information from band 1
b1proj = image.select('B1').projection()
pprint(b1proj.getInfo())

# Get scale (in meters) information from band 1
b1scale = image.select('B1').projection().nominalScale()
pprint(b1scale.getInfo())

# Note that different bands can have different projections and scale
b8scale = image.select('B8').projection().nominalScale()
pprint(b8scale.getInfo())

# Get a list of all metadata properties
# image.getInfo() return a dict object, the key 'properites' store the metadata of image
properties = image.getInfo()['properties']
pprint(properties.keys())

# Get a specific metadata property
cloudiness = image.get('CLOUD_COVER').getInfo()
print(cloudiness)

# Get the timestamp and covert it to a date
date = ee.Date(image.get('system:time_start')).getInfo()
pprint(date)