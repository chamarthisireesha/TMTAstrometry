# example
from inputs import * 
import numpy as np
from error_calculator import Error_calculator
import matplotlib.pyplot as plt
Nref = np.arange(1, 100, dtype=int)
c=0
Nref.shape
error = np.zeros(Nref.shape)
field['NSci'] = 1
field['Nfield'] = 1
field['rsep'] = 15
field['rdref'] = 15
for k in Nref:
	field['Nref'] = k
	output = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,'Absolute Astrometry')
	error[c] = output['Astrometry error']
	c=c+1
plt.plot(Nref,error)
plt.xlabel('Number of reference stars',fontsize=14)
plt.ylabel('astrometry error ($\mu as$)',fontsize=14)
plt.show()
