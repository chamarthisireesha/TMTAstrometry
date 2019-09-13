# calculate absolute astrometry error

from inputs import fred
import formulae as f
import math

# calaculations as per old spreadsheet
# sigma_x = sigma_sci
# sigma_t = sigma_ref
# sigma_t['Opto-mechanical errors']['NGS position errors'] = sigma_NGS['Opto-mechanical errors']['NGS position errors']

def abs_astrometry(global_inputs,field,sigma_sci,sigma_field,sigma_ref,sigma_NGS):
	sigma_sci['Residual turbulence errors']['Diff TTJ plate scale'] = 150/(global_inputs['T'])**0.5
	field['rsep'] = field['rdref']
	
	if field['Nref']<3:
		noise_err = f.A2(sigma_sci['Focal-plane measurement errors']['Noise'])
		noise_cal_err = f.A2(sigma_sci['Focal-plane measurement errors']['Noise calibration errors'])
		pix_blur = f.A2(sigma_sci['Focal-plane measurement errors']['Pixel blur'])
		pix_irr = f.A2(sigma_sci['Focal-plane measurement errors']['Pixel irregularities'])
		det_nl = f.A2(sigma_sci['Focal-plane measurement errors']['Detector non-linearity'])
		PSF_rec = f.A2(sigma_sci['Focal-plane measurement errors']['PSF reconstruction'])
		conf_err = f.A2(sigma_sci['Focal-plane measurement errors']['Confusion'])

		FP_err = noise_err + noise_cal_err + pix_blur + pix_irr + det_nl + PSF_rec + conf_err
		sigma_field['Focal-plane measurement errors']['Subtotal'] = math.sqrt(FP_err)

	
		NGS_pos_err = f.PS1(sigma_NGS['Opto-mechanical errors']['NGS position errors'],field,global_inputs)
		NF_IR_optics = f.A2(sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS optics'])
		NF_IR_SFE = f.A2(sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS surfaces'])
		QS_dist = f.A2(sigma_sci['Opto-mechanical errors']['Quasi_static distortions'])
		tel_opt = f.A2(sigma_sci['Opto-mechanical errors']['Telescope optics'])
		rot_err = f.A2(sigma_sci['Opto-mechanical errors']['Rotator errors'])
		Act_spikes = f.A2(sigma_sci['Opto-mechanical errors']['Actuators diffr spikes'])
		Vib_err = f.A2(sigma_sci['Opto-mechanical errors']['Vibrations'])
		cop_atm_eff = f.A2(sigma_sci['Opto-mechanical errors']['Coupling atm effects'])

		opt_mech_err =NGS_pos_err+  NF_IR_optics + NF_IR_SFE + QS_dist + tel_opt + rot_err + Act_spikes + Vib_err + cop_atm_eff
		sigma_field['Opto-mechanical errors']['Subtotal'] = math.sqrt(opt_mech_err)

		achr_diff_ref = f.A2(sigma_sci['Atmospheric refraction errors']['Achromatic differential refraction'])
		DSO_err = f.A2(sigma_sci['Atmospheric refraction errors']['Dispersion obj spectra'])
		DAC_err = f.A2(sigma_sci['Atmospheric refraction errors']['Dispersion atm conditions'])
		DADC_pos = f.A2(sigma_sci['Atmospheric refraction errors']['Dispersion ADC position'])
		Disp_var = f.A2(sigma_sci['Atmospheric refraction errors']['Dispersion variability'])

		Atm_ref_err = achr_diff_ref + DSO_err + DAC_err + DADC_pos + Disp_var
		sigma_field['Atmospheric refraction errors']['Subtotal'] = math.sqrt(Atm_ref_err)
	
		Diff_TTJ_PS = f.A2(sigma_sci['Residual turbulence errors']['Diff TTJ plate scale'])

		Diff_TTJ_HO = f.A2(sigma_sci['Residual turbulence errors']['Diff TTJ higher order'])
		PSF_irr = f.A2(sigma_sci['Residual turbulence errors']['PSF irregularities'])
		PSF_HE = f.A2(sigma_sci['Residual turbulence errors']['Halo effect'])
		TC_var = f.A2(sigma_sci['Residual turbulence errors']['Turb conditions variability'])

		Res_turb_err = Diff_TTJ_PS + Diff_TTJ_HO + PSF_irr + PSF_HE +TC_var
		sigma_field['Residual turbulence errors']['Subtotal'] = math.sqrt(Res_turb_err)

		pos_err = f.PS1(sigma_ref['Reference obj n catalog errors']['Position errors'],field,global_inputs)
		PM_err = f.PS1(sigma_ref['Reference obj n catalog errors']['Proper motion errors'],field,global_inputs)
		Abr_grav_err = f.PS1(sigma_ref['Reference obj n catalog errors']['Aberration grav deflection'],field,global_inputs)
		other_err = f.PS1(sigma_ref['Reference obj n catalog errors']['Other'],field,global_inputs)

		ref_obj_cat_err = pos_err + PM_err + Abr_grav_err + other_err
		sigma_field['Residual turbulence errors']['Subtotal'] = math.sqrt(ref_obj_cat_err)

	elif field['Nref']>=3:
		noise_err = f.A1(sigma_sci['Focal-plane measurement errors']['Noise'],sigma_sci['Focal-plane measurement errors']['Noise'],field,fred)
		noise_cal_err = f.A1(sigma_sci['Focal-plane measurement errors']['Noise calibration errors'],sigma_sci['Focal-plane measurement errors']['Noise calibration errors'],field,fred)
		pix_blur = f.A1(sigma_sci['Focal-plane measurement errors']['Pixel blur'],sigma_sci['Focal-plane measurement errors']['Pixel blur'],field,fred)
		pix_irr = f.A1(sigma_sci['Focal-plane measurement errors']['Pixel irregularities'],sigma_sci['Focal-plane measurement errors']['Pixel irregularities'],field,fred)
		det_nl = f.A1(sigma_sci['Focal-plane measurement errors']['Detector non-linearity'],sigma_sci['Focal-plane measurement errors']['Detector non-linearity'],field,fred)
		PSF_rec = f.A1(sigma_sci['Focal-plane measurement errors']['PSF reconstruction'],sigma_sci['Focal-plane measurement errors']['PSF reconstruction'],field,fred)
		conf_err = f.A1(sigma_sci['Focal-plane measurement errors']['Confusion'],sigma_sci['Focal-plane measurement errors']['Confusion'],field,fred)

		FP_err = noise_err + noise_cal_err + pix_blur + pix_irr + det_nl + PSF_rec + conf_err
		sigma_field['Focal-plane measurement errors']['Subtotal'] = math.sqrt(FP_err)

	
		NGS_pos_err = 0
		NF_IR_optics = f.A1(sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS optics'],sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS optics'],field,fred)
		NF_IR_SFE = f.A1(sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS surfaces'],sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS surfaces'],field,fred)
		QS_dist = f.A1(sigma_sci['Opto-mechanical errors']['Quasi_static distortions'],sigma_sci['Opto-mechanical errors']['Quasi_static distortions'],field,fred)
		tel_opt = f.A1(sigma_sci['Opto-mechanical errors']['Telescope optics'],sigma_sci['Opto-mechanical errors']['Telescope optics'],field,fred)
		rot_err = f.A1(sigma_sci['Opto-mechanical errors']['Rotator errors'],sigma_sci['Opto-mechanical errors']['Rotator errors'],field,fred)
		Act_spikes = f.A1(sigma_sci['Opto-mechanical errors']['Actuators diffr spikes'],sigma_sci['Opto-mechanical errors']['Actuators diffr spikes'],field,fred)
		Vib_err = f.A1(sigma_sci['Opto-mechanical errors']['Vibrations'],sigma_sci['Opto-mechanical errors']['Vibrations'],field,fred)
		cop_atm_eff = f.A1(sigma_sci['Opto-mechanical errors']['Coupling atm effects'],sigma_sci['Opto-mechanical errors']['Coupling atm effects'],field,fred)

		opt_mech_err =NGS_pos_err+  NF_IR_optics + NF_IR_SFE + QS_dist + tel_opt + rot_err + Act_spikes + Vib_err + cop_atm_eff
		sigma_field['Opto-mechanical errors']['Subtotal'] = math.sqrt(opt_mech_err)

		achr_diff_ref = f.A1(sigma_sci['Atmospheric refraction errors']['Achromatic differential refraction'],sigma_sci['Atmospheric refraction errors']['Achromatic differential refraction'],field,fred)
		DSO_err = f.A1(sigma_sci['Atmospheric refraction errors']['Dispersion obj spectra'],sigma_sci['Atmospheric refraction errors']['Dispersion obj spectra'],field,fred)
		DAC_err = f.A1(sigma_sci['Atmospheric refraction errors']['Dispersion atm conditions'],sigma_sci['Atmospheric refraction errors']['Dispersion atm conditions'],field,fred)
		DADC_pos = f.A1(sigma_sci['Atmospheric refraction errors']['Dispersion ADC position'],sigma_sci['Atmospheric refraction errors']['Dispersion ADC position'],field,fred)
		Disp_var = f.A1(sigma_sci['Atmospheric refraction errors']['Dispersion variability'],sigma_sci['Atmospheric refraction errors']['Dispersion variability'],field,fred)

		Atm_ref_err = achr_diff_ref + DSO_err + DAC_err + DADC_pos + Disp_var
		sigma_field['Atmospheric refraction errors']['Subtotal'] = math.sqrt(Atm_ref_err)
	
		Diff_TTJ_PS = 0

		Diff_TTJ_HO = f.A1(sigma_sci['Residual turbulence errors']['Diff TTJ higher order'],sigma_sci['Residual turbulence errors']['Diff TTJ higher order'],field,fred)
		PSF_irr = f.A1(sigma_sci['Residual turbulence errors']['PSF irregularities'],sigma_sci['Residual turbulence errors']['PSF irregularities'],field,fred)
		PSF_HE = f.A1(sigma_sci['Residual turbulence errors']['Halo effect'],sigma_sci['Residual turbulence errors']['Halo effect'],field,fred)
		TC_var = f.A1(sigma_sci['Residual turbulence errors']['Turb conditions variability'],sigma_sci['Residual turbulence errors']['Turb conditions variability'],field,fred)

		Res_turb_err = Diff_TTJ_PS + Diff_TTJ_HO + PSF_irr + PSF_HE 
		sigma_field['Residual turbulence errors']['Subtotal'] = math.sqrt(Res_turb_err)

		pos_err = f.PS2(sigma_ref['Reference obj n catalog errors']['Position errors'],field,global_inputs)
		PM_err = f.PS2(sigma_ref['Reference obj n catalog errors']['Proper motion errors'],field,global_inputs)
		Abr_grav_err = f.PS2(sigma_ref['Reference obj n catalog errors']['Aberration grav deflection'],field,global_inputs)
		other_err = f.PS2(sigma_ref['Reference obj n catalog errors']['Other'],field,global_inputs)

		ref_obj_cat_err = pos_err + PM_err + Abr_grav_err + other_err
		sigma_field['Residual turbulence errors']['Subtotal'] = math.sqrt(ref_obj_cat_err)

	pixel_error = math.sqrt(FP_err + opt_mech_err + Atm_ref_err + Res_turb_err )

	astrometry_error = math.sqrt(FP_err + opt_mech_err + Atm_ref_err + Res_turb_err + ref_obj_cat_err)

	error_subtotals ={ 'Focal-plane measurement errors': sigma_field['Focal-plane measurement errors']['Subtotal'],
						'Opto-mechanical errors': sigma_field['Opto-mechanical errors']['Subtotal'],
						'Atmospheric refraction errors': sigma_field['Atmospheric refraction errors']['Subtotal'],
						'Residual turbulence errors':sigma_field['Residual turbulence errors']['Subtotal'],
						'Pixel coordinate error': pixel_error,
						'Total plate scale error': sigma_ref['Reference obj n catalog errors']['Subtotal'],
						'Astrometry error': astrometry_error}

	return error_subtotals