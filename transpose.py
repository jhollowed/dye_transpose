import sys
import pdb
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def transpose_input(file_in, out_name=None, num_replicates=5, num_dyes=4, 
                    remove_header=True):
	'''
	Once again transposes some kinda lame science data into some 
	other kinda lame science data

	Paramters
	---------
	file_in : string
		Path to input csv file
	out_name : string
		Name of output file. Defaults to a rename of the input data, at the 
		same location
	num_replicates : int, optional
		Number of replicates described in the input data, defaults to 5.
	num_dyes : int, optional
		Number of dyes described in the input data, defaults to 4.
	remove_header : bool, optional
		Whether or not to remove the first row of the input data.
	'''

	# read input data, chop off header row if desired
	datin = np.genfromtxt(file_in, delimiter=',')
	if(remove_header):
		datin = datin[1:]
		print('header removed')

	# gather data dimensions, quantities
	num_wavelengths = len(datin[0])
	num_readings = num_replicates * num_dyes
	num_concentrations = int(len(datin) / num_readings)
	print('gathered data dimensions')
	print('number of wavelengths: {}'.format(num_wavelengths))
	print('number of readings: {}'.format(num_readings))
	print('number of concentrations: {}'.format(num_concentrations))

	# build index matrix
	# each row of this matrix will contain the indices of rows from the input data that
	# should be concatenated to form each new (longer) row of the transformed output
	idx_matrix = np.reshape(np.arange(0, num_readings), 
                            (num_dyes, num_replicates)).T
	print('generated index matrix with dimensions {}x{}'.format(num_replicates, num_dyes))
	
	# build template for output data	
	nrows = num_replicates*num_concentrations
	ncols = num_wavelengths*num_dyes
	datout = np.zeros((nrows, ncols))
	print('generated output data with dimensions {}x{}'.format(nrows, ncols))
    
	# populate output template
	print('\nperforming transformation...')
	for i in range(num_concentrations):
		print('concetration {}...'.format(i))
		for j in range(num_replicates):
			this_idx = idx_matrix[j] + num_readings*i
			datout[i*num_replicates + j] = datin[this_idx].flatten()
	
	# save output file	
	if out_name is None:
		out_name = '{}.transformed.csv'.format(file_in.split('.csv')[0])
	np.savetxt(out_name, datout, delimiter=',')
	print('\nsaved to {}'.format(out_name))


# ===========================================================================


if __name__ == '__main__':
	
	# usage: python transpose.py {input filename} {output_filename}
	out_name = None
	f = sys.argv[1]
	if(len(sys.argv) == 3): out_name = sys.argv[2]
	transpose_input(f, out_name)	
