# example
from inputs import * 
import numpy as np
from error_calculator import Error_calculator
import matplotlib.pyplot as plt


label_size = 12

plt.rcParams['xtick.labelsize'] = label_size 

plt.rcParams['ytick.labelsize'] = label_size 

plt.rcParams['axes.labelsize'] = label_size 

plt.rcParams['axes.titlesize'] = label_size +2
plt.rcParams['lines.linewidth'] = 3.0 
SNR = np.arange(1, 100,1)
c=0

error = np.zeros(SNR.shape)
field['NSci'] = 1
field['Nref']=10000
field['Nfield']=10000

global_inputs['SNR-fie-id']=100
global_inputs['SNR-ref-id']=250
global_inputs['wavelength-id']='K'

for k in SNR:
	global_inputs['SNR-sci-id'] = k
	output = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,'Differential astrometry (relative to field stars)')
	error[c] = output['Astrometry error']
	c=c+1
plt.plot(SNR,error)
plt.xlabel('SNR')
plt.ylabel(r'astrometry error ($\mu$as)')
plt.show()
