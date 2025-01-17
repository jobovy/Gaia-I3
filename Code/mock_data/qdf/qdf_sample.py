"""
NAME:
    qdf sample

PURPOSE:
    A function that samples location and veloicty under quasi-isothermal
    density function
    
WARNING:
    In order for this module to run, you need to run a modified
    galpy quasiisothermaldf.py first, since it assumes a sampleV interpolate
    function that the standard galpy does not have.
    
HISTORY:
    2018-07-05 - Written - Samuel Wong
    2017-07-16 - Added sample velocity and use the interpolation sample location
"""
import sys
sys.path.append('../sampling')
sys.path.append('../../tools')
from tools import cyl_to_rect, to_physical_units
from sampling import sample_location_interpolate
import numpy as np
import time as time_class
#import qdf related things
from galpy.potential import MWPotential2014
from galpy.actionAngle import actionAngleAdiabatic
aA= actionAngleAdiabatic(pot=MWPotential2014,c=True)
# set up qdf
# qdf not imported from galpy since I am running a modified galpy in console
qdf= quasiisothermaldf(1./3.,0.2,0.1,1.,1.,pot=MWPotential2014,aA=aA,cutcounter=True)

start = time_class.time()
#sample location
# get the maximum of qdf
qdf_max = 1.2*qdf.density(0.9375, 0)
# sample R from 7.5 kpc to 8.5 kpc; sample z from -0.5 kpc to 0.5 kpc
# let phi range from -arctan(0.5/8) to arctan(0.5/8)
location = sample_location_interpolate(qdf.density, 1700000, 0.9375, 1.0625,
                                       -0.0625, 0.0625, -0.0624, 0.0624, 
                                       df_max = qdf_max, pixel_R = 0.01,
                                       pixel_z = 0.01)
# sample velocity
# get the R, z and phi colum
R,z,phi = location.T
#sample v interpolate
Rz_v = qdf.sampleV_interpolate(R, z, R_pixel = 0.01, z_pixel = 0.01)
R, z, vR, vT, vz = Rz_v.T
# convert to cartesian
coord_rect = cyl_to_rect(R, vR, vT, z, vz, phi)
# convert from natural to physics 
physical_rect = to_physical_units(coord_rect)

#get current date
date = time_class.localtime(time_class.time())[0:3]
#save data
np.save("qdf sample cartesian physical, date={}.npy".format(str(date)), physical_rect)

end = time_class.time()
print('time =', end - start)

