from skimage.io import imread

import matplotlib.pyplot as plt

import imageio.v2 as imageio
'''
img = imageio.imread("C:\\Users\\Andrei Necsulea\\Downloads\\testere\\scatter.png")

img_data = imageio.get_reader(img)

plt.imshow(img_data)

plt.show()
'''
import imageio.v3 as iio

metadata = iio.imread("C:\\Users\\Andrei Necsulea\\Downloads\\testere\\scatter.png")
print(metadata)  # "RGB"