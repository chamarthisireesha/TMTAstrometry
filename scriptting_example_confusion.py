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
Confusion = np.array([1.5,1,2,8,12,90,110,224,361,500,1000,1200,1250])

mag_sci=np.array([10.5,11.8,13,14,15,16,17,18,19,20,21,22,23])
c=0

error = np.zeros(Confusion.shape)
global_inputs['T']=3600
field['rref-sci']=3
global_inputs['rref']=0.3
field['NSci'] = 1
field['Nref']=400
field['Nfield']=10000
global_inputs['SNR-sci']=200

global_inputs['SNR_fie']=680
global_inputs['SNR_ref']=4800
global_inputs['wavelength-id']='K'

for k in np.arange(Confusion.size):
	sigma_sci['Focal-plane measurement errors']['Confusion'] = Confusion[k]
	global_inputs['SNR-sci-id']=mag_sci[k]
	output = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,'Differential astrometry (relative to field stars)')
	error[c] = output['Astrometry error']
	c=c+1
plt.plot(mag_sci,error,'o-')
plt.xlabel('K magnitude')
plt.ylabel(r'astrometry error ($\mu$as)')
plt.show()
