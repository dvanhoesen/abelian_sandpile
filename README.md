# abelian_sandpile
Bak-Tang-Wiesenfeld Abelian Sandpile Model

# Description
Python scripts to simulate the Abelian Sandpile model, also known as the Bak-Tang-Wiesenfeld model. A square grid is developed with random numbers between 0 and 3. For N iterations, a random grid point is selected and 1 is added to the grid value. If the grid value becomes 4, then the grid point is reduced to 0 and the value of 4 is given to the points top, right, bottom, and left neighbors, which are each increased by a value of 1. If any of the neighboring grid points becomes a value of 4, then that point is reduced to 0 and its neighboring points are bumped by 1. This condintues until there are no remaining points with a value of 4. This routine creates a cascade which can spread throughout the grid system. Matplotlib ion() and draw() functions are used to enable dynamic figure updating in the iteration loops. Four plots are created in the simulation: (1) simulation grid with colors representing values between 0 and 4, (2) a reduced grid showing the cascade points alone along with the number of times a grid point was involved in the cascade (blue = less, red = more), (3) the average grid value for each iteration of the simulation, and (4) a distribution of the magnitude of the cascade (the number of grid points involved in the cascade). 

The average grid value saturates to a value just above 2 due to the dissipative boundary conditions. You can think of the model as a pile of sand with the grid boundaries as a the edge of shelf or table where if the sand falls off the edge, it no longer interacts with the rest of the system. 

# Files
 - images\ - example images for generating a video from the saved simulation images
 - sandpile_2D.py - main Python code for simulating the Abelian Sandpile model. Uses Numpy for matrix operations and Matplotlib for image generation and dynamic display. OpenCV is used for building the video file. 
 - images_to_video.py - using the images optionally saved in the sandpile_2D.py to build an avi video using OpenCV. 
 - requirements.txt - simulation requirements (Numpy, Matplotlib, and OpenCV)
 - README.md - this file

# Notes
 - Tested on Windows 10 with Python 3.9.12
 - OpenCV installed via
   - pip install opencv-python
