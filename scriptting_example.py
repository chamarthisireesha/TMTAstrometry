# example
from inputs import * 
import numpy as np
from error_calculator import Error_calculator
import matplotlib.pyplot as plt

import plotly.graph_objs as go
import numpy as np
from scipy import interpolate



field['Nsci'] = 1
field['Nfield'] = 1
field['Nref'] = 100
field['rref-sci'] = 15


arr_Kbb=np.loadtxt('Kbb.csv',delimiter=',')
TMT_data = np.loadtxt('TMT.csv',delimiter=',')
# f1= interpolate.interp2d(arr_Kbb[:,0],arr_Kbb[:,1],arr_Kbb[:,2], kind='cubic') 
X = arr_Kbb[0::36,0]
Y = arr_Kbb[0:36,1]
Z = np.reshape(arr_Kbb[:,2], (100,36))
f2= interpolate.RectBivariateSpline(X,Y,Z)   


KMag = TMT_data[:,0];
confusion = TMT_data[:,1];

# SNR1 = f1(KMag,3600)
SNR2 = np.zeros((13,1))
i = 0
for K in KMag:
	SNR2[i] = f2(K,3600)
	i = i+1



output = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,'Absolute Astrometry')
	
plt.plot(KMag,SNR2)
plt.xlabel('Number of reference stars',fontsize=14)
plt.ylabel('astrometry error ($\mu as$)',fontsize=14)
plt.show()
