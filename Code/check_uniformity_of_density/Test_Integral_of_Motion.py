from Integral_of_Motion import *
import numpy as np
from astropy.coordinates import SkyCoord, CartesianRepresentation, CartesianDifferential
import astropy.units as u
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014
from Uniformity_Evaluation import grad

# global variables
# for the position, I took an example from online, the answer is (2, pi/6, 4)
x = np.sqrt(3)
y = 1.
z = 4.
# for the velocity, I chose the test to see whether the total velocity is the same, which is clealry 1 here
vx = np.sqrt(1 / 3)
vy = np.sqrt(1 / 3)
vz = np.sqrt(1 / 3)


def test_cartesian_to_cylindrical(x, y, z, vx, vy, vz):
    R, phi, z, vR, vT, vz = cartesian_to_cylindrical(x, y, z, vx, vy, vz)
    print('cylindrical position: ({},{},{})'.format(R, phi, z))
    print('cylindrical velocity: ({},{},{})'.format(vR, vT, vz))
    v = np.sqrt(vR**2 + vT**2 + vz**2)
    print('net velocity = ', v)
    
def test_cylindrical_to_cartesian(x, y, z, vx, vy, vz):
    R, phi, z, vR, vT, vz = cartesian_to_cylindrical(x, y, z, vx, vy, vz)
    new_x, new_y, new_z, new_vx, new_vy, new_vz = cylindrical_to_cartesian(R, phi, z, vR, vT, vz)
    print(x, y, z, vx, vy, vz)
    print(new_x, new_y, new_z, new_vx, new_vy, new_vz)
    
def test_energy_and_momentum(x,y,z,vx,vy,vz):
    # test whether energy and momentum changed during an orbit
    # know that they are conserved
    coord = np.array([x,y,z,vx,vy,vz])
    e_initial = Energy(coord)
    momentum_initial = L_z(coord)
    R, phi, z, vR, vT, vz = cartesian_to_cylindrical(x, y, z, vx, vy, vz)
    o =  Orbit(vxvv = [R, vR, vT, z, vz, phi])
    ts = np.linspace(0,1000,100000)
    o.integrate(ts,MWPotential2014)
    t = 1000
    new_coord = np.array([o.x(t), o.y(t), o.z(t), o.vx(t), o.vy(t), o.vz(t)])
    e_final = Energy(new_coord)
    momentum_final = L_z(new_coord)
    print('initial energy = {}, final energy = {}'.format(e_initial, e_final))
    print('initial momentum = {}, final momentum = {}'.format(momentum_initial, momentum_final))
    
def test_energy_momentum_of_sun():
    o = Orbit() # create sun's orbit
    o.turn_physical_off()
    ts = np.linspace(0,1000,100000)
    o.integrate(ts,MWPotential2014)
    print('galpy energy = ', o.E())
    coord = np.array([o.x(),o.y(),o.z(),o.vx(),o.vy(),o.vz()])
    print('my energy = ', Energy(coord))
    print(o.E() == Energy(coord))
    print('galpy momentum = ', o.L()[0][2])
    print('my momentum = ', L_z(coord))
    print(o.L()[0][2] == L_z(coord))
    
def test_analytic_energy_gradient():
    point1 = np.array([x, y, z, vx, vy, vz])
    point2 = np.array([x*1.1, y*1.2, z*1.3, vx*1.4, vy*1.5, vz*1.6])
    points = np.array([point1, point2])
    numeric_del_E = grad(Energy, 6)
    print('numeric del E 1 = ', numeric_del_E(point1))
    print('numeric del E 2 = ', numeric_del_E(point2))
    print('analytic del E =', del_E(points))
    
def test_analytic_momentum_gradient():
    point1 = np.array([x, y, z, vx, vy, vz])
    point2 = np.array([x*1.1, y*1.2, z*1.3, vx*1.4, vy*1.5, vz*1.6])
    points = np.array([point1, point2])
    numeric_del_Lz = grad(L_z, 6)
    print('numeric del L_z 1 = ', numeric_del_Lz(point1))
    print('numeric del L_z 2 = ', numeric_del_Lz(point2))
    print('analytic del L_z =', del_Lz(points))
    
#test_cartesian_to_cylindrical(x, y, z, vx, vy, vz)
#print()
#test_cylindrical_to_cartesian(1,2,3,4,5,6)
#print()
#test_energy_and_momentum(x, y, z, vx, vy, vz)
#print()
#test_energy_momentum_of_sun()
#print()
test_analytic_energy_gradient()
test_analytic_momentum_gradient()
