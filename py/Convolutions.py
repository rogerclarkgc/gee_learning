import ee
from ee import mapclient

ee.Initialize()

# Load and display an image
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Define a boxcar or low-pass kernel
boxcar = ee.Kernel.square(radius=7, units="pixels", normalize=True)

# Smooth the image by convolving with boxcar kernel
smooth = image.convolve(boxcar)
#mapclient.centerMap(-122.1651, 37.5128, 9)
#mapclient.addToMap(smooth, {'bands': ['B5', 'B4', 'B3'],'max': 0.5}, "smoothed")

# Define a Laplacian, or edge-dectection kernel
laplacian = ee.Kernel.laplacian8(normalize=False)

# Apply the edge-detection kernel
edgy = image.convolve(laplacian)
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'max': 0.5,
             'format': 'png'}
#mapclient.centerMap(-122.1651, 37.5128, 9)
#mapclient.addToMap(edgy, vizParams, 'edges')

# Create a list of weights for a 9x9 kernel
list1 = [1 for i in range(9)]
# The center of the kernel is zero
centerList = [1 for i in range(4)] + [0] + [1 for i in range(4)]
# Assemble a list of lists: the 9x9 kernel weights as a 2-D matrix
lists = [list1 for i in range(4)] + [centerList] + [list1 for i in range(4)]
# Create the kernel from the weights
kernel = ee.Kernel.fixed(width=9,
                         height=9,
                         weights=lists,
                         x=-4,
                         y=-4,
                         normalize=False)
print(kernel.getInfo())