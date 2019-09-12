# The function takes inputs from UI, calculates additional parameters from the UI inputs 
# and sends  them to approriate function to calculate the astrometry error
from Diff_astro_field_stars import diff_fie
from Diff_astro_sci_objects import diff_sci
from Absolute_astrometry import abs_astrometry
import copy


def Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,astrometry_type):
	sigma_sci['Focal-plane measurement errors']['Noise'] = 3400000000*global_inputs['wavelength']/global_inputs['SNR_sci']
	sigma_sci['Residual turbulence errors']['Diff TTJ higher order'] = 105/(global_inputs['T'])**0.5
	sigma_sci['Residual turbulence errors']['PSF irregularities'] = 55/(global_inputs['T'])**0.5
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
	return error




