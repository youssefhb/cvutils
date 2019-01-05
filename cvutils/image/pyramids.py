import numpy as np
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2
import sys

from skimage import data
from skimage import io
from skimage.transform import pyramid_gaussian


def main(argv):
    # construct the argument parser and parse the arguments
	
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="path to input image")
	args = ap.parse_args()

	# Image pyramids using opencv
	opencv_image(args.image)
	skimage_pyramid(args.image)    

def  skimage_pyramid(imageName): # RGB
	image = io.imread(imageName)
	rows, cols, dim = image.shape
	pyramid = tuple(pyramid_gaussian(image, downscale=2, multichannel=True))
	sizes = tuple(p.shape for p in pyramid)
	a = np.asarray(sizes)
	max_row = np.sum(a[1:],axis=0)[0]
	print(max_row)
	
	composite_image = np.zeros((max_row, cols + cols // 2, 3), dtype=np.double)

	composite_image[:rows, :cols, :] = pyramid[0]

	i_row = 0
	for p in pyramid[1:]:
		n_rows, n_cols = p.shape[:2]
		composite_image[i_row:i_row + n_rows, cols:cols + n_cols] = p
		i_row += n_rows

	fig, ax = plt.subplots()
	ax.imshow(composite_image)
	plt.show()


def  opencv_image(imageName): # BGR
	
	# Load an color image
	img = cv2.imread(imageName)
	cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
	cv2.imshow('Image',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	height,width = img.shape[:2]
	print(height,width)
		

	# The pyramid_gaussian function takes an image and yields successive images shrunk by a constant scale factor.
	# Image pyramids are often used, e.g., to implement algorithms for denoising, texture discrimination, and scale-invariant detection.
	#imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	pyramid = tuple(pyramid_gaussian(img, downscale=2.0, multichannel=True))



	for p in pyramid[1:-1]:
		print(p.shape,str(pyramid.index(p)))
		height,width = p.shape[:2]
		resized_image = cv2.resize(img, (width,height),interpolation = cv2.INTER_AREA) 
		#cv2.namedWindow('Image'+str(pyramid.index(p)),cv2.WINDOW_OPENGL)
		cv2.namedWindow('Opencv'+str(pyramid.index(p)),cv2.WINDOW_AUTOSIZE)
		cv2.imshow('Opencv'+str(pyramid.index(p)),resized_image)
		cv2.waitKey(0)

	cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])
