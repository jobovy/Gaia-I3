import numpy as np
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014
from tools import *
import os, sys
outer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(outer_path)
from check_uniformity_of_density.Integral_of_Motion import *

def test_natural_unit(t):
    o = Orbit() # create sun's orbit
    o.turn_physical_off() # make galpy use natural coordinate
    ts = np.linspace(0,100,1000)
    o.integrate(ts,MWPotential2014)
    natural_coord = np.array([o.x(t),o.y(t),o.z(t),o.vx(t),o.vy(t),o.vz(t)])
    natural_energy = o.E(t)
    natural_momentum = o.L(t)[0][2]
    
    o.turn_physical_on() # make galpy use physical coordinate
    physical_coord = np.array([o.x(t),o.y(t),o.z(t),o.vx(t),o.vy(t),o.vz(t)])
    my_coord = to_natural_units(np.array([physical_coord]))[0]
    my_energy = Energy(my_coord)
    my_momentum = L_z(my_coord)
    
    
    print('galpy natural coord = ', natural_coord)
    print('my natural coord = ', my_coord)
    print('galpy energy = ', natural_energy)
    print('my energy = ', my_energy)
    print('galpy natural momentum = ', natural_momentum)
    print('my momentum = ', my_momentum)
    
def test_frame_conversion(x, y, z, vx, vy, vz):
    point = np.array([x, y, z, vx, vy, vz])
    print(galactocentric_to_galactic(galactic_to_galactocentric(point)))
    print(galactic_to_galactocentric(galactocentric_to_galactic(point)))

def test_create_meshgrid(xy_min, xy_max, xy_spacing, z_min, z_max, z_spacing,
                         vxy_min, vxy_max, vxy_spacing, vz_min, vz_max, vz_spacing):

    result = create_meshgrid(xy_min, xy_max, xy_spacing, z_min, z_max, z_spacing,
                    vxy_min, vxy_max, vxy_spacing, vz_min, vz_max, vz_spacing)
    print('The grid is :')
    for point in result:
        print(point)
    print('Grid size is', result.shape[0])
    
def test_std_cut(number_of_std_cut):
    samples = np.random.randn(1000,6)
    print("Shape of random data:", samples.shape)
    print("Length of random data:", len(samples))
    print(std_cut(samples, number_of_std_cut))

test_natural_unit(38)
#test_frame_conversion(1.,2.,3.5,6.7, 8.3,3.2)
#test_create_meshgrid(-1, 1, 1, -1, 1, 1, 8, 9, 1, 10, 11, 1)
test_std_cut(3)
