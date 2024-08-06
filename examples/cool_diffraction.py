import diffractsim
diffractsim.set_backend("CUDA") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import MonochromaticField,PolychromaticField,ApertureFromImage,Lens, cf, mm, cm, nm

import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing

plt.ioff()


def test_function(i):
    """F = PolychromaticField(
	    spectrum=1.5 * cf.illuminant_d65,
	    extent_x=20 * mm,
	    extent_y=20 * mm,
	    Nx=1600,
	    Ny=1600,
	)"""
	
    F = MonochromaticField(
	    wavelength = 632.8 * nm, extent_x=20. * mm, extent_y=20. * mm, Nx=4096, Ny=4096
	)

    F.add(ApertureFromImage("./apertures/cool-diffraction.jpg", image_size=(15 * mm, 15 * mm), simulation = F))
    F.add(Lens(f = 25*cm, radius = .2*cm))
    F.propagate(z=i/10*cm)
    rgb = F.get_colors()
    F.plot_colors(rgb, xlim=[-10*mm, 10*mm], ylim=[-10*mm, 10*mm])
    plt.savefig('/home/bberto/Documents/cooler-with-radius-diffraction-%s.png' % str(i/10))

for i in range(0,750,1000):
    jobs = []
    p = multiprocessing.Process(target=test_function,args=(i,))
    jobs.append(p)
    p.start()
    p = multiprocessing.Process(target=test_function,args=(i+750,))
    jobs.append(p)
    p.start()
    print("Starting %i & %i" % (i, i+750))

    # Iterate through the list of jobs and remove one that are finished, checking every second.
    while len(jobs) > 0:
        jobs = [job for job in jobs if job.is_alive()]
        time.sleep(1)
	
