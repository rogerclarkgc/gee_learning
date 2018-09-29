from pprint import pprint
import ee
from ee import mapclient

ee.Initialize()

# Load two 5-year Landsat 7 composites.
landsat1999 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003')
landsat2008 = ee.Image('LANDSAT/LE7_TOA_5YEAR/2008_2012')

# Compute NDVI the hard way
ndvi1999 = landsat1999.select('B4').subtract(landsat1999.select('B3'))\
    .divide(landsat1999.select('B4').add(landsat1999.select('B3')))

# Compute NDVI the easy way
ndvi2008 = landsat2008.normalizedDifference(['B4', 'B3'])

# Compute difference of ndvi
ndvidiff = ndvi2008.subtract(ndvi1999)
print('#####ndvidiff#####')
pprint(ndvidiff.getInfo())


# Compute the multi-band difference image
diff = landsat2008.subtract(landsat1999)
print('#####diff#####')
pprint(diff.getInfo())
print('#####diff.pow(2)#####')
pprint(diff.pow(2).getInfo())

# Expressions

# Load a Landsat 8 image
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Compute the EVI using an expression
evi = image.expression(expression='2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
                       opt_map={
                           'NIR': image.select('B5'),
                           'RED': image.select('B4'),
                           'BLUE': image.select('B2')
                       })
vizParam = {'min': -1, 'max': 1, 'palette': ['FF0000', '00FF00']}
mapclient.centerMap(-122.1225, 37.5217, 10)
mapclient.addToMap(evi, vizParam, 'evi')
print('#####evi#####')
pprint(evi.getInfo())

# Another way to apply a expression, using 'b(index)' to refer a band
evi = image.expression('2.5 * ((b(5) - b(4)) / (b(5) + 6 * 1.0 * b(4) - 7.5 * b(2) + 1.0))')
#mapclient.centerMap(-122.1225, 37.5217, 10)
#mapclient.addToMap(evi, vizParam, 'evi')