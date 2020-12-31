# The function takes inputs from UI, calculates additional parameters from the UI inputs 
# and sends  them to approriate function to calculate the astrometry error
from Diff_astro_field_stars import diff_fie
from Diff_astro_sci_objects import diff_sci
from Absolute_astrometry import abs_astrometry
import copy
from scipy import interpolate
import numpy as np


def Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,astrometry_type):
	sigma_sci['Focal-plane measurement errors']['Noise'] = 3400000000*global_inputs['wavelength']/global_inputs['SNR_sci']
	sigma_sci['Residual turbulence errors']['Diff TTJ higher order'] = 105/(global_inputs['T'])**0.5
	sigma_sci['Residual turbulence errors']['PSF irregularities'] = 55/(global_inputs['T'])**0.5

	if global_inputs['wavelength']==0.000000928:
				arr_Zbb=np.loadtxt('Zbb.csv',delimiter=',')
				X = arr_Zbb[0::36,0]
				Y = arr_Zbb[0:36,1]
				Z = np.reshape(arr_Zbb[:,2], (100,36))
				f= interpolate.RectBivariateSpline(X,Y,Z)  
                # f = interpolate.interp2d(arr_Zbb[:,0],arr_Zbb[:,1],arr_Zbb[:,2], kind='cubic')
	elif global_inputs['wavelength']==0.00000109:
				arr_Ybb=np.loadtxt('Ybb.csv',delimiter=',')
				X = arr_Ybb[0::36,0]
				Y = arr_Ybb[0:36,1]
				Z = np.reshape(arr_Ybb[:,2], (100,36))
				f= interpolate.RectBivariateSpline(X,Y,Z)  
                # f = interpolate.interp2d(arr_Ybb[:,0],arr_Ybb[:,1],arr_Ybb[:,2], kind='cubic')          
	elif global_inputs['wavelength']==0.00000127:
				arr_Jbb=np.loadtxt('Jbb.csv',delimiter=',')
				X = arr_Jbb[0::36,0]
				Y = arr_Jbb[0:36,1]
				Z = np.reshape(arr_Jbb[:,2], (100,36))
				f = interpolate.RectBivariateSpline(X,Y,Z)  
                # f= interpolate.interp2d(arr_Jbb[:,0],arr_Jbb[:,1],arr_Jbb[:,2], kind='cubic')           
	elif global_inputs['wavelength']==0.000001629:
				arr_Hbb=np.loadtxt('Hbb.csv',delimiter=',')
				X = arr_Hbb[0::36,0]
				Y = arr_Hbb[0:36,1]
				Z = np.reshape(arr_Hbb[:,2], (100,36))
				f = interpolate.RectBivariateSpline(X,Y,Z)  
                # f = interpolate.interp2d(arr_Hbb[:,0],arr_Hbb[:,1],arr_Hbb[:,2], kind='cubic')          
	else:
				arr_Kbb=np.loadtxt('Kbb.csv',delimiter=',')
				X = arr_Kbb[0::36,0]
				Y = arr_Kbb[0:36,1]
				Z = np.reshape(arr_Kbb[:,2], (100,36))
				f = interpolate.RectBivariateSpline(X,Y,Z)  
                # f= interpolate.interp2d(arr_Kbb[:,0],arr_Kbb[:,1],arr_Kbb[:,2], kind='cubic') 



	if 'Mag_sci' in global_inputs.keys():
		global_inputs['SNR_sci'] = f(global_inputs['Mag_sci'],global_inputs['T'])

	if 'Mag_fie' in global_inputs.keys():
		global_inputs['SNR_fie'] = f(global_inputs['Mag_fie'],global_inputs['T'])

	if 'Mag_ref' in global_inputs.keys():
		global_inputs['SNR_ref'] = f(global_inputs['Mag_ref'],global_inputs['T'])
    


	for l in sigma_sci:
		sigma_sci[l]['Subtotal'] = 0

	sigma_field = copy.deepcopy(sigma_sci)
	sigma_field['Focal-plane measurement errors']['Noise'] = 3400000000*global_inputs['wavelength']/global_inputs['SNR_fie']
	sigma_field['Residual turbulence errors']['Diff TTJ plate scale'] = 150/(global_inputs['T'])**0.5/28*field['rref-sci']
	for l in sigma_field:
		sigma_field[l]['Subtotal'] = 0


	sigma_ref = copy.deepcopy(sigma_sci)
	sigma_ref['Focal-plane measurement errors']['Noise'] = 3400000000*global_inputs['wavelength']/global_inputs['SNR_ref']
	sigma_ref['Residual turbulence errors']['Diff TTJ plate scale'] = 150/(global_inputs['T'])**0.5/28*field['rref-sci']
	sigma_ref['Reference obj n catalog errors'] =  RefObjNCatErr
	sigma_ref['Reference obj n catalog errors']['Proper motion errors'] = 500*global_inputs['dt_epoch']
	sigma_ref['Reference obj n catalog errors']['Measurement Uncertainty'] = 0
	for l in sigma_ref:
		sigma_ref[l]['Subtotal'] = 0


	if astrometry_type == 'Differential astrometry (relative to field stars)':
		error = diff_fie(global_inputs,field,sigma_sci,sigma_field,sigma_ref,sigma_NGS)
	elif astrometry_type == 'Differential astrometry (science objects relative to each other)':
		error = diff_sci(global_inputs,field,sigma_sci,sigma_field,sigma_ref,sigma_NGS)
	elif astrometry_type == 'Absolute Astrometry':
		error = abs_astrometry(global_inputs,field,sigma_sci,sigma_field,sigma_ref,sigma_NGS)
	else:
		print('No option selected. Something went wrong')
	# print(error)

	for key in error: 
		error[key] = round(error[key], 4) 

	return error




