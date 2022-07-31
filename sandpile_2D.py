"""
Description:
2D Abelian sandpile model with rectangular grid points

Owner: Daniel Van Hoesne
Created by: Daniel Van Hoesen
Creation Date: 07/29/2022

Notes:

References:
"""

######################
### Imports
######################

# System
import sys
import os

# Analysis
import numpy as np

# Plotting
import matplotlib.pyplot as plt
from matplotlib import colors


######################
### Definitions
######################

def getNeighbors(x, y):

	# Find the grid neighbors of x and y
	# Remove edge neighbor points (i.e., dissipative boundary conditions)
	# Return the neighbors

	# Find all neighbors regardless of edge points
	xs = np.array([x-1, x, x, x+1])
	ys = np.array([y, y-1, y+1, y])

	# Find indexes that correspond to inner neighbors only
	x_idx = np.where((xs >= 0) & (xs < grid_size))
	y_idx = np.where((ys >= 0) & (ys < grid_size))

	# Intersect the lists (i.e., keep overlapping indexes from the index arrays)
	keep_idx = np.intersect1d(x_idx, y_idx)

	# Apply the found indexes on the neighbors list
	xs = xs[keep_idx]
	ys = ys[keep_idx]

	return xs, ys


######################
### Constants
######################

grid_size = 30
iterations = 5000
pause_time = 0.0001

flag_save = True
flag_display = False

mycolors = ['#CCD3FC', '#99A7F8', '#667AF5', '#334EF1', '#EE4B2B']
savepath = 'images' + os.path.sep

max_cascade = 100
num_bins = 50
bin_cutoffs = np.linspace(0, max_cascade, num_bins+1, endpoint=True)

start_bin_middle = ( max_cascade / num_bins ) / 2
last_bin_middle = max_cascade - start_bin_middle

bins = np.linspace(start_bin_middle, last_bin_middle, num_bins, endpoint=True)



######################
### Main
######################

if __name__ == '__main__':

	# Define the cascade size bin buckets 
	bin_counts = np.zeros(len(bins))

	# initialize 8-bit numpy array (integers 0-255) with random numbers between 0 and 3
	grid = np.random.randint(0, high=4, size=(grid_size, grid_size), dtype=np.int8)
	grid_iter = np.zeros((grid_size, grid_size), dtype=np.int8)

	# Initialize arrays for the averages at each time step and the timesteps
	avg = np.zeros(iterations+1)
	time = np.arange(0,iterations+1)

	avg[0] = np.mean(grid)
	print("Starting Average grid value: {}".format(avg[0]))

	# Define the custom discrete colormap
	cmap = colors.ListedColormap(mycolors)

	# Initiize matplotlib figure and turn on GUI event loop
	plt.ion()
	fig, ax = plt.subplots(2, 2, figsize=(12, 10))

	# Add main Abelian sandpile model image
	im = ax[0,0].imshow(grid, interpolation=None, cmap=cmap, vmin=0, vmax=4, aspect='auto')

	# Turn off axis 
	ax[0,0].axis('off')

	# Add colorbar
	#cbar = fig.colorbar(im, ax=ax[0,0], ticks=[0,1,2,3,4], fraction=0.046, pad=0.04)
	#cbar.ax.set_yticklabels(['0','1','2','3','4'])

	# Add affected imshow plot of the cascade size
	imc = ax[0,1].imshow(grid_iter, interpolation=None, cmap='seismic', vmin=0, vmax=10, aspect='auto')

	# Turn off axis 
	ax[0,1].axis('off')

	# Add the average value plot
	line, = ax[1,0].plot(time[0], avg[0], '-', color='blue', linewidth=2)
	ax[1,0].set_ylabel("Average Grid Value", fontsize=12)
	ax[1,0].set_xlabel("Iteration Number", fontsize=12)
	ax[1,0].set_xlim([0, time[-1]*1.05])
	ax[1,0].set_ylim([1.45, 2.15])

	# Add the cascade size plot
	cs_size = ax[1,1].bar(x=bin_cutoffs[0:-1], height=bin_counts, width=np.diff(bin_cutoffs), align='edge', fc='blue')
	ax[1,1].set_ylabel("Number of Cascades (Log10)", fontsize=12)
	ax[1,1].set_xlabel("Cascade Magnitude", fontsize=12)
	ax[1,1].set_ylim([0, 1.05])
	ax[1,1].set_yticks([])

	plt.subplots_adjust(wspace=0.1, hspace=0.1)

	# Draw the figure and pause
	if flag_display:
		plt.draw()
		plt.pause(pause_time)

	fig_cnt = 0

	# Randomly bump an index point for the number of iterations
	for i in range(iterations):

		# initialize variable to quantify the cascade size
		cs = 0

		# Get random index in the grid
		[idx, idy] = np.random.randint(0, high=grid_size, size=2)

		# Increase the randomly selected grid point by 1
		grid[idx, idy] += 1

		# set the imshow image with the new data and draw
		im.set_data(grid)

		if flag_display:
			plt.draw()
			plt.pause(pause_time)

		if flag_save:
			figname = savepath + str(fig_cnt).zfill(8) + '.png'
			fig.savefig(figname, dpi=100, pad_inches=0.3, bbox_inches='tight')
			fig_cnt += 1

		if grid[idx, idy] >= 4:
			counter = 1
			idx4 = np.array([[idx],[idy]])
			grid_iter[idx, idy] += 1
			cs += 1

		else:
			counter = 0
		
		# continue looping while the counter is not zero
		while counter != 0:

			# Loop through all indexes
			for j in range(counter):
				cs += 1

				# Set index to 0
				idx = idx4[0][j]
				idy = idx4[1][j]
				grid[idx, idy] = 0
				grid_iter[idx, idy] += 1

				# Get index neighbors
				xnbr, ynbr = getNeighbors(idx, idy)

				# Increase the neighbor grid points by 1
				grid[xnbr, ynbr] += 1

				# Update the figure
				im.set_data(grid)
				imc.set_data(grid_iter)

				if flag_display:
					plt.draw()
					plt.pause(pause_time)

				if flag_save:
					figname = savepath + str(fig_cnt).zfill(8) + '.png'
					fig.savefig(figname, dpi=100, pad_inches=0.3, bbox_inches='tight')
					fig_cnt += 1

			# Find all indexes where grid value is 4
			idx4 = np.where(grid>=4)
			counter = len(idx4[0])

		# Calculate the new average grid value
		avg[i+1] = np.average(grid)

		# bin the cascade size by finding the index where the size should be placed
		# only capture indexes with lower magnitude value than the max set value
		try:
			idx = np.amin(np.where(bin_cutoffs > cs)) - 1
			bin_counts[idx] += 1
		except:
			continue

		# Add 1 to the bin counts and take the log10 (add 1 to avoid log10(0) = -inf error)
		bc = np.log10(np.copy(bin_counts) + 1)

		# Use a relative bin counts metric so the figure stays between 0 and 1
		bin_counts_relative = bc / np.amax(bc)

		# Update the line plot
		line.set_xdata(time[0:i+1])
		line.set_ydata(avg[0:i+1])

		# Update the histogram
		cs_size.remove()
		cs_size = ax[1,1].bar(x=bin_cutoffs[0:-1], height=bin_counts_relative, width=np.diff(bin_cutoffs), align='edge', fc='blue')

		if flag_display:
			plt.draw()

		grid_iter = np.zeros((grid_size, grid_size), dtype=np.int8)

	#fig.savefig('test.png', dpi=300, pad_inches=0.3, bbox_inches='tight')
	#plt.pause(3)