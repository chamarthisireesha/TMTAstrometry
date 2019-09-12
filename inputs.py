# These inputs are inputs to calculations in Absolute_astrometry.py, Diff_astro_sci_objects.py
# Diff_astro_field_stars.py. The inputs are either 1) predefined constants, user inputs from UI or derived from user inputs in  function error_calculator.py
import copy

global_inputs = {
"wavelength" : 0.0000022,
"SNR_sci" : 200,
"SNR_fie" : 100,
"SNR_ref" : 250,
"rngs" : 50,
"rref" : 17,
"T" : 100,
"dt_epoch" : 1.5}

field = {
"Nref" : 7,
"rsep" : 0, # old spreadsheet
"Nfield" : 100,
"Nsci" : 1,
"Nngs": 3,
"rref-sci":10,
"rdref": 1} # should be labelled rdsci

sigma_sci = {'Focal-plane measurement errors':{
		'Noise' : 1,
		'Noise calibration errors': 4,
		'Pixel blur': 1,
		'Pixel irregularities': 2,
		'Detector non-linearity': 1,
		'PSF reconstruction': 5,
		'Confusion': 5,
		'Subtotal' : 0,
	},
	'Opto-mechanical errors':{
		'NGS position errors': 0,
		'NFIAROS_IRIS optics': 8,
		'NFIAROS_IRIS surfaces': 7,
		'Quasi_static distortions': 5,
		'Telescope optics': 5,
		'Rotator errors': 3,
		'Actuators diffr spikes': 1,
		'Vibrations': 5,
		'Coupling atm effects': 3,
		'Subtotal' : 0
	},
	'Atmospheric refraction errors':{
		'Achromatic differential refraction': 2,
		'Dispersion obj spectra': 5,
		'Dispersion atm conditions': 5,
		'Dispersion ADC position': 1,
		'Dispersion variability': 2,
		'Subtotal' : 0
	},
	'Residual turbulence errors':{
		'Diff TTJ plate scale': 0.0,
		'Diff TTJ higher order': 10.5,
		'PSF irregularities': 5.5,
		'Halo effect': 3,
		'Turb conditions variability': 1,
		'Subtotal' : 0
	}
}



RefObjNCatErr = {
	'Measurement Uncertainty' : 0,
	'Position errors' : 1000,
	'Proper motion errors': 0,
	'Aberration grav deflection': 1,
	'Other': 1,
	'Total Plate Scale Error': 0
	}


sigma_NGS ={"Opto-mechanical errors":{"NGS position errors": 2000}}

fred = 1 # used in old spreadsheet


