import ee
from ee import mapclient

ee.Initialize()


"""
Earth Engine has several special methods for estimating spatial texture.
When the image is discrete valued (not floating point),
you can use image.entropy() to compute the entropy in a neighborhood:
"""
# Load a high-resolution NAIP image.
image = ee.Image('USDA/NAIP/DOQQ/m_3712213_sw_10_1_20140613')
# Get the NIR band
nir = image.select('N')

# Define a neighborhood with a kernel
square = ee.Kernel.square(radius=4)

# Compute entropy and display
entropy = nir.entropy(square)

#mapclient.centerMap(-122.44829, 37.76664, 17)
#mapclient.addToMap(entropy,
#                   {'min': 1,
#                    'max': 5,
#                    'palette': ['0000CC', 'CC0000']},
#                   'entropy')

"""
Note that the NIR band is scaled to 8-bits prior to calling entropy()
since the entropy computation takes discrete valued inputs.
The non-zero elements in the kernel specify the neighborhood.

Another way to measure texture is with a gray-level co-occurrence matrix (GLCM).
Using the image and kernel from the previous example, compute the GLCM-based contrast as follows:
"""

# Compute the gray-level co-occurence matrix (GLCM), get contrast.
# Roger: contrast image seems not work right, the returned image is different from javascript code editor
glcm = nir.glcmTexture(size=4)
contrast = glcm.select('N_contrast')


"""
Many measures of texture are output by image.glcm().
For a complete reference on the outputs, see Haralick et al. (1973) and Conners et al. (1984).
Local measures of spatial association such as Geary's C (Anselin 1995) can be computed
in Earth Engine using image.neighborhoodToBands(). Using the image from the previous example:
"""

# Create a list of weights for a 9x9 kernel.
lst = [1 for _ in range(9)]
# The center of the kernel is zero.
centerList = [1 for _ in range(9)]
centerList[4] = 0
# Assemble a list of lists: the 9x9 kernel weights as a 2-D matrix
lists = [lst for _ in range(9)]
lists[4] = centerList
# Create the kernel from the weights.
# Non-zero weights represent the spatial neighborhood
kernel = ee.Kernel.fixed(9, 9, lists, -4, -4, False)

# Convert the neighborhood into multiple bands.
neighs = nir.neighborhoodToBands(kernel)

# Compute local Geary's C, a measure of spatial association
gearys = nir.subtract(neighs)\
    .pow(2)\
    .reduce(ee.Reducer.sum())\
    .divide(81)


mapclient.centerMap(-122.44829, 37.76664, 17)
mapclient.addToMap(gearys,
                   {'min': 20,
                    'max': 2500,
                    'palette': ['0000CC', 'CC0000']},
                    "Geary's C")