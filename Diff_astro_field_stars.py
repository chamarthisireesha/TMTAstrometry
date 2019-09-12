# Calculate differential astrometry error using field objects.
# from inputs import fred
# import formulae as f
def diff_fie(global_inputs,field,sigma_sci,sigma_field,sigma_ref,sigma_NGS):
	
	## field density dependent calculations

	# Confusion 0 for spare fields
	if field['Nref'] < 6:
		sigma_field['Focal-plane measurement errors']['Confusion'] = 0
		sigma_sci['Focal-plane measurement errors']['Confusion'] = 0

	# NGS position error for ref stars less than 3
	if field['Nref'] < 3:
		sigma_field['Opto-mechanical errors']['NGS position errors'] = sigma_NGS['Opto-mechanical errors']['NGS position errors']*field['rref-sci']/global_inputs['rngs']
	# ref stars 3 or more
	if field['Nref'] >=3:
		sigma_field['Opto-mechanical errors']['NGS Position errors'] = 0

	# Halo effect for spares field is 0
	if field['Nref']<6:
		sigma_field['Residual turbulence errors']['Halo effect'] = 0

	# proper motion error for very spare fields
	if field['Nref']<3:
		sigma_ref['Reference obj n catalog errors']['Position errors'] = 0



	## quarature subtotal of errors for field stars,ref stars and science object
	for m, n in sigma_sci.items(): # sigma sci
		subtotal = 0
		err = 0
		for l in n:
			err = sigma_sci[m][l]
			subtotal = subtotal+err**2

		sigma_sci[m]['Subtotal'] = (subtotal)**0.5

	for m, n in sigma_field.items(): # sigma field
		subtotal = 0
		err = 0
		for l in n:
			err = sigma_field[m][l]/((field['Nfield'])**0.5)
			subtotal = subtotal+err**2

		sigma_field[m]['Subtotal'] = (subtotal)**0.5
		sigma_field[m]['Subtotal'] = (sigma_field[m]['Subtotal']**2 + sigma_sci[m]['Subtotal']**2)**0.5



	for m, n in sigma_ref.items(): # sigma ref
		subtotal = 0
		err = 0
		for l in n:
			err = sigma_ref[m][l]
			subtotal = subtotal+err**2

		sigma_ref[m]['Subtotal'] = (subtotal)**0.5

	# Measurement uncertainty
	meas_unc = (sigma_ref['Focal-plane measurement errors']['Subtotal']**2 + sigma_ref['Opto-mechanical errors']['Subtotal']**2  + sigma_ref['Atmospheric refraction errors']['Subtotal']**2 + sigma_ref['Residual turbulence errors']['Subtotal']**2)**0.5
	sigma_ref['Reference obj n catalog errors']['Measurement Uncertainty'] = meas_unc
	sigma_ref['Reference obj n catalog errors']['Subtotal'] = 0
	# ref object errors for sparse fields
	subtotal = 0
	err=0
	if field['Nref']<3:
		for l in sigma_ref['Reference obj n catalog errors']:
			if l == 'Measurement Uncertainty':
				err = sigma_ref['Reference obj n catalog errors'][l]/(field['Nref'])**0.5
			else:
				err = sigma_ref['Reference obj n catalog errors'][l]
			subtotal = subtotal+err**2


	# ref object errors for dense fields
	if field['Nref']>=3:
		for l in sigma_ref['Reference obj n catalog errors']:
			if l == 'Measurement Uncertainty':
				err = sigma_ref['Reference obj n catalog errors'][l]/(field['Nref'])**0.5
			else:
				err = sigma_ref['Reference obj n catalog errors'][l]*((3/field['Nref'])**0.5)*field['rdref']/global_inputs['rref']
			subtotal = subtotal+err**2

	sigma_ref['Reference obj n catalog errors']['Subtotal'] = (subtotal)**0.5

	pixel_error = 0
	for l in sigma_field:
		pixel_error = sigma_field[l]['Subtotal']**2 + pixel_error

	pixel_error = pixel_error**0.5

	## total astrometry error 
	astrometry_error = (pixel_error**2 + sigma_ref['Reference obj n catalog errors']['Subtotal']**2)**0.5

	error_subtotals ={ 'Focal-plane measurement errors': sigma_field['Focal-plane measurement errors']['Subtotal'],
						'Opto-mechanical errors': sigma_field['Opto-mechanical errors']['Subtotal'],
						'Atmospheric refraction errors': sigma_field['Atmospheric refraction errors']['Subtotal'],
						'Residual turbulence errors':sigma_field['Residual turbulence errors']['Subtotal'],
						'Pixel coordinate error': pixel_error,
						'Total plate scale error': sigma_ref['Reference obj n catalog errors']['Subtotal'],
						'Astrometry error': astrometry_error}

	return [error_subtotals]