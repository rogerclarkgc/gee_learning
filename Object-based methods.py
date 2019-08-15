import ee
from ee import mapclient

ee.Initialize()

"""
For treating landscape elements as objects, Earth Engine contains several methods.
Specifically, when an image has distinct patches identified by unique pixel values,
use image.connectedPixelCount() to compute the number of pixels in each patch
and image.connectedComponents() to label each patch with a unique identifier.
The unique identifiers can then be used to enumerate the patches
and analyze the distribution of size or some other quality of interest.
The following computes the size and unique identifiers of hot patches in a surface temperature image:
"""

# Load a Landsat 8 image and display the thermal band.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Threshold the thermal band to find "hot" objects.
hotspots = image.select('B10').gt(303)

# Mask 'cold' pixels.
hotspots = hotspots.updateMask(hotspots)

# Compute the number of pixels in each patch
patchsize = hotspots.connectedPixelCount(256, False)

# Uniquely label the patches and visualize
patchid = hotspots.connectedComponents(ee.Kernel.plus(1), 256)
mapclient.centerMap(-122.1899, 37.5010, 13)
mapclient.addToMap(patchid.randomVisualizer(), {}, 'patches')

"""
In the previous example, note that the maximum patch size is set to 256 pixels by the arguments to the connectedPixelCount()
and connectedComponents() methods. The connectivity is also specified by the arguments,
in the former method by a boolean and in the latter method by an ee.Kernel. In this example,
only four neighbors are considered for each pixel.
"""
