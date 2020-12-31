import numpy as np
from scipy import interpolate
arr_Zbb=np.loadtxt('Zbb.csv',delimiter=',')
f = interpolate.interp2d(arr_Zbb[:,0],arr_Zbb[:,1],arr_Zbb[:,2], kind='cubic')
SNR = f(20,100)