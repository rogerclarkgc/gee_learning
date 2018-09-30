import ee
from ee import mapclient

ee.Initialize()

# Load a Landsat 8 image
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Create NDVI and NDWI spectral indices
ndvi = image.normalizedDifference(['B5', 'B4'])
ndwi = image.normalizedDifference(['B3', 'B5'])

# Create a binary layer using logical operations
# using ee.Image.bitwise_and to calculate AND operation
bare = ndvi.lt(0.2).bitwise_and(ndwi.lt(0))

# Another way
image = ee.Image.cat([ndvi, ndwi])
print(image.bandNames().getInfo())
bare2 = image.expression("(b('nd') < 0.2) && (b('nd_1') < 0)")

#mapclient.centerMap(-122.3578, 37.7726, 12)
#mapclient.addToMap(bare2.updateMask(bare2), {}, 'bare2')

# Load a 2012 nightlights image
nl2012 = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012')
lights = nl2012.select('stable_lights')

# Define arbitrary thresholds on the 6-bit stable lights band
zones = lights.gt(30).add(lights.gt(55)).add(lights.gt(62))

# Display the threshold image as three district zone near Paris
palette = ['000000', '0000FF', '00FF00', 'FF0000']

# Create zones using an expression
zonesExp = nl2012.expression("(b('stable_lights')>62) ? 3" +\
                             ": (b('stable_lights')>55) ? 2" +\
                             ": (b('stable_lights')>30) ? 1" +\
                             ": 0")

#mapclient.centerMap(2.373, 48.8683, 8)
#mapclient.addToMap(zonesExp, {'min': 0, 'max': 3, 'palette': palette}, 'development zones')

# Load a cloudy Landsat 8 image
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20130603')

# Load another image to relace the cloudy pixels
replacement = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20130416')

# Compute a cloud score band
cloud = ee.Algorithms.Landsat.simpleCloudScore(image).select('cloud')

# Set cloudy pixels to the other image
replaced = image.where(cloud.gt(10), replacement)

mapclient.centerMap(-122.151, 37.451, 9)
mapclient.addToMap(replaced,
                   {'bands': ['B5', 'B4', 'B3'],
                              'min': 0,
                              'max': 0.5},
                   'clouds replaced')