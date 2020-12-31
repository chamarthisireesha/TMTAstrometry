# example
from inputs import * 
import numpy as np
from error_calculator import Error_calculator
import matplotlib.pyplot as plt
from scipy import interpolate

label_size = 12

plt.rcParams['xtick.labelsize'] = label_size 

plt.rcParams['ytick.labelsize'] = label_size 

plt.rcParams['axes.labelsize'] = label_size 

plt.rcParams['axes.titlesize'] = label_size +2
plt.rcParams['lines.linewidth'] = 3.0 

TMT_data = np.loadtxt('TMT.csv',delimiter=',')
mag_sci = TMT_data[:,0];
Confusion = TMT_data[:,1];
# Confusion = np.array([1.5,1,2,8,12,90,110,224,361,500,1000,1200,1250])

# mag_sci=np.array([10.5,11.8,13,14,15,16,17,18,19,20,21,22,23])
c=0

error = np.zeros(Confusion.shape)
global_inputs['T']=3600
field['rref-sci']=3
global_inputs['rref']=17
field['Nref']=10
field['Nfield']=10000
global_inputs['SNR-sci']=200

global_inputs['SNR_fie']=680
global_inputs['SNR_ref']=4800
global_inputs['wavelength-id']='K'

arr_Kbb=np.loadtxt('Kbb.csv',delimiter=',')
X = arr_Kbb[0::36,0]
Y = arr_Kbb[0:36,1]
Z = np.reshape(arr_Kbb[:,2], (100,36))
f2= interpolate.RectBivariateSpline(X,Y,Z)  

for k in np.arange(Confusion.size):
	sigma_sci['Focal-plane measurement errors']['Confusion'] = Confusion[k]
	global_inputs['SNR-sci']=f2(mag_sci[k],3600)
	# global_inputs['SNR-sci']=200
	output = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,'Differential astrometry (relative to field stars)')
	print(output)
	error[c] = output['Astrometry error']
	c=c+1
plt.plot(mag_sci,Confusion,'o-',label = 'conffusion error')
plt.plot(mag_sci,error,'o-',label = 'Total Atroemtry error')
plt.yscale('log')
plt.xlabel('K magnitude')
plt.ylabel('$\mu as$')
plt.title('rref = 17 arcsec, Nref = 10')
plt.legend()
plt.show()

