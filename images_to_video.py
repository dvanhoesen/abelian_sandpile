"""
Description:
2D Abelian sandpile model with rectangular grid points
convert images to video using OpenCV

Owner: Daniel Van Hoesne
Created by: Daniel Van Hoesen
Creation Date: 07/30/2022

Notes:
images are ordered by frame number with left padded zeros (i.e., zfill())

References:
https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html
"""

######################
### Imports
######################

# System
import sys
import os
import glob

# Video
import cv2


######################
### Definitions
######################



######################
### Constants
######################

basepath = os.getcwd() + os.path.sep
image_path = basepath + "images" + os.path.sep

# Note that the savename file format should match the fourcc_codec type
savename = basepath + "sandpile_2d.mp4"

# Video frames per second
fps = 64


######################
### Main
######################

if __name__ == '__main__':


	# Select all images in the image path
	files = glob.glob(image_path + "*.png")

	# Number of files
	n = len(files)

	# Loop through all images (loaded in correct order automaticallyl by glob)

	cnt = 0
	for file in files:
		img = cv2.imread(file)

		# If first image, then get the image properties
		if cnt == 0:
			height, width, layers = img.shape
			print("Image height: {}".format(height))
			print("Image width: {}".format(width))
			print("Number of Image layers: {}".format(layers))

			# Create the video object
			fourcc_codec = cv2.VideoWriter_fourcc(*'mp4v')
			video = cv2.VideoWriter(savename, fourcc_codec, fps, (width,height))

		video.write(img)
		
		# Display progress to the user
		if cnt%1000 == 0 and cnt > 0:
			percent_completed = round((cnt / n)*100, 2)
			print(percent_completed, " %")

		cnt += 1
	
	 
	# Release the video
	cv2.destroyAllWindows()
	video.release()