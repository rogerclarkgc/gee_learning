import ee
from ee import mapclient

# Initialize ee
ee.Initialize()

# Load a Landsat 8 top-of-atmosphere reflectance image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Convert the RGB bands to the HSV color spcace
hsv = image.select(['B4', 'B3', 'B2']).rgbToHsv()

# Swap in the panchromatic band and convert back to RGB
sharpened = ee.Image.cat([hsv.select('hue'),
                          hsv.select('saturation'),
                          image.select('B8')]).hsvToRgb()

#mapclient.centerMap(-122.44829, 37.76664, 13)
#mapclient.addToMap(sharpened,
#                  {'min': 0,
#                   'max': 0.25,
#                   'gamma': [1.3, 1.3, 1.3]},
#                  'pan-sharpened')


# Load a Landsat 6 image and select the bands we want to unmix
bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
image = ee.Image('LANDSAT/LT05/C01/T1/LT05_044034_20080214').select(bands)

# Define spectral endmembers
urban = [88, 42, 48, 38, 86, 115, 59]
veg = [50, 21, 20, 35, 50, 110, 23]
water = [51, 20, 14, 9, 7, 116, 4]

# Unmix the map
fractions = image.unmix([urban, veg, water])
mapclient.centerMap(-122.1899, 37.5010, 10)
mapclient.addToMap(fractions, {}, 'unmixed')