import ee
from ee import mapclient
from pprint import pprint

ee.Initialize()

## Morphological Operations ##

# Load a landsat 8 image, select NIR band, threshold
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')\
    .select(4).gt(0.2)

# Define a kernel
kernel = ee.Kernel.circle(radius=1)

# Perform an erosion followed by a dilation, display
opened = image\
        .focal_min(kernel=kernel, iterations=2)\
        .focal_max(kernel=kernel, iterations=2)

#mapclient.centerMap(-122.1899, 37.5010, 13)
#mapclient.addToMap(opened, {}, 'opened')


## Gradients ##

image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')

# Compute the image gradient in the X and Y direction
xyGrad = image.gradient()

# Compute the magnitude of the gradient
gradient = xyGrad.select('x').pow(2.0)\
    .add(xyGrad.select('y').pow(2.0)).sqrt()

# Compute the direction of the gradient
direction = xyGrad.select('y').atan2(xyGrad.select('x'))

# Display the results

#mapclient.centerMap(-122.054, 37.7295, 10)
#mapclient.addToMap(direction, {'min': -2, 'max': 2, 'format': 'png'}, 'direction')
#mapclient.addToMap(gradient, {'min': -7, 'max': 7, 'format': 'png'}, 'gradient')

## Edge detection

image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')

# Perform Canny edge detection and display the result.
canny = ee.Algorithms.CannyEdgeDetector(image, threshold=10, sigma=1)
#mapclient.centerMap(-122.054, 37.7295, 10)
#mapclient.addToMap(canny, {}, 'canny')

# Perform Hough transform of the Canny result and display.
hough = ee.Algorithms.HoughTransform(image=canny,
                                     inputThreshold=100,
                                     lineThreshold=100,
                                     smooth=True)

#mapclient.centerMap(-122.054, 37.7295, 10)
#mapclient.addToMap(hough, {}, 'hough')

# `zeroCrossing() method`

# Define a "fat" Gaussian kernel
fat = ee.Kernel.gaussian(radius=3,
                         sigma=3,
                         units="pixels",
                         normalize=True,
                         magnitude=-1)

# Define a "skinny" Gaussian kernel
skinny = ee.Kernel.gaussian(radius=3,
                            sigma=1,
                            units="pixels",
                            normalize=True)

# Compute a difference-of-Gaussian (DOG) kernel
dog = fat.add(skinny)

# Compute the zero corossing of second derivative, display

zeroXings = image.convolve(dog).zeroCrossing()
mapclient.centerMap(-122.054, 37.7295, 10)
mapclient.addToMap(zeroXings.updateMask(zeroXings),
                   {'palette': 'FF0000'},
                   'zero crossings')