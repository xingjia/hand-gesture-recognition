from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from scipy.signal import medfilt as med_filter
from scipy.ndimage.filters import gaussian_filter
import cv2
import os
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

def normalize_to_gray_scale(old_array, min, max):
	for elm in old_array:
		elm = (elm - min) * 255 / (max - min)
	return old_array

def preprocess_images(rootdir, image_each_row):
	np.set_printoptions(threshold='nan')

	grid = gridspec.GridSpec(image_each_row, image_each_row, wspace=0.0, hspace=0.0)
	for subdir, dirs, files in os.walk(rootdir):
		counter = 0
		for file in files:
			if counter > image_each_row * image_each_row - 1:
				continue
			image_path = os.path.join(subdir, file)
			if ("confi" in image_path or not image_path.endswith('.png')):
				continue
			if ("depth" in image_path):
		   		confi_path = image_path.replace("depth_", "confi_")
			
			print "Reading ", image_path	
			im = Image.open(image_path)
			conf = Image.open(confi_path)

			imarray = np.array(im)
			confarray=np.array(conf)

			# median filter and gaussian filter
			imarray = med_filter(imarray, 3)
			imarray = gaussian_filter(imarray, 0.5)

			#remove low confidence and high dist pixels
			max_dist = np.amax(imarray);
			low_conf_ind =  confarray < 150
			high_dep_ind = imarray > np.median(imarray) - 40
			print np.array_str(np.median(imarray))
			imarray[low_conf_ind] = 0
			imarray[high_dep_ind] = 0
			
			sub = plt.subplot(grid[counter/image_each_row, counter%image_each_row])
			sub.axes.get_xaxis().set_visible(False)
			sub.axes.get_yaxis().set_visible(False)
			sub.imshow(imarray, cmap=cm.gray)
			counter+= 1
	
	f = open('testarray.txt', 'w')
		
	f.write(np.array_str(imarray,  max_line_width='nan'))
	f.close()
	plt.axis('off')
	plt.show()


if __name__ == "__main__":
	rootdir = '/Users/xingjia/Development/hand-gesture/SSF/ssf14--depth/3'
	image_each_row = sys.argv[1]
	preprocess_images(rootdir, int(image_each_row))
