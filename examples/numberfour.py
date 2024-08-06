import diffractsim
diffractsim.set_backend("CUDA") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import MonochromaticField,PolychromaticField,ApertureFromImage,Lens ,cf, mm, cm, nm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.ioff()

for i in range(0,51,1):
	"""F = MonochromaticField(
	    wavelength = 632.8 * nm, extent_x=20. * mm, extent_y=20. * mm, Nx=2048, Ny=2048
	)"""
	
	F = PolychromaticField(
	    spectrum=1.5 * cf.illuminant_d65,
	    extent_x=20 * mm,
	    extent_y=20 * mm,
	    Nx=2048,
	    Ny=2028,
	)

	F.add(ApertureFromImage("./apertures/4.png", image_size=(15 * mm, 15 * mm), simulation = F))
	F.add(Lens(f = 25*cm))
	F.propagate(z=i*cm)
	rgb = F.get_colors()
	F.plot_colors(rgb, xlim=[-10*mm, 10*mm], ylim=[-10*mm, 10*mm])
	plt.savefig('/home/bberto/Documents/numberfour%s-poly.png' % str(i))
	
#tried to recreate it but in CUDA and with an image of a four instead

