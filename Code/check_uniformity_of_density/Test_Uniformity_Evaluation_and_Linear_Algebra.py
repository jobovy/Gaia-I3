from Linear_Algebra import *
from Uniformity_Evaluation import *
import numpy as np
from sympy import Matrix
from Integral_of_Motion import Energy, L_z

def f(array):
    x = array[0]
    y = array[1]
    z = array[2]
    return 2*x*y + 3*y*z + z**2

def g(array):
    x, y, z = array.T
    return 2*x*y + 3*y*z + z**2

# global variables
point = np.array([1., 1., 2.])
gradient = np.array([2., 8., 7.])
W = orthogonal_complement(np.array([gradient]))
x = np.sqrt(3)
y = 1.
z = 4.
vx = np.sqrt(1 / 3)
vy = np.sqrt(1 / 3)
vz = np.sqrt(1 / 3)
a = np.array([x,y,z,vx,vy,vz])


def test_evaluate_uniformity_and_orthogonal_complement(f, point, W):
    # I hand calculated the gradient at the given point, ask orthogonal_complement function to calculate its orthogonal
    # space. Then ask evaluate_uniformit to find the dot product against the othogonal space
    # the answer should be 2 numbers very close to zero.
    # success implies that both orthogonal_complement and gradient have to work properly
    #del_f = gradient(f, np.size(point))
    print('dot product between gradient and its orthonormal space:', evaluate_uniformity(f, point, W))


def test_orthonormality(W):
    # test whether the subspace output by orthogonal_complement are actually orthonormal
    # get dimensions of W
    m, n = np.shape(W)
    for i in range(m):
        print('norm of w[{}] = {}'.format(i, Matrix.norm(Matrix(W[i]))))

    for i in range(m):
        for j in range(m-1):
            if j != i:
                print('w[{}] dot w[{}] = {}'.format(i, j, np.dot(W[i],W[j])))
                
                
def test_compatibility_with_integral_of_motion():
    # get the gradient of energy and momentum at the point
    del_E = grad(Energy, np.size(a))
    del_Lz = grad(L_z, np.size(a))
    del_E_a = del_E(a)
    del_Lz_a = del_Lz(a)
    print('energy vector = {}, momentum vector = {}'.format(del_E_a, del_Lz_a))
    
def test_normalize_vector():
    b = normalize_vector(a)
    print('original vector a = ', a)
    print('normalized vector b = ', b)
    print('b/a = ', b/a)
    print('norm(b) = ', np.sum(b**2))
    
def test_gradient():
    print('point = ', point)
    del_f = grad(f, 3)
    del_f_x = del_f(point)
    print('grad(point) = ', del_f_x)
    print('point = ', point)
    
def test_grad_multi():
    points = np.array([[1., 1., 2.],[2., 4., 6.]])
    print('points = ', points)
    print('grad(points) = ', grad_multi(g, points))

def test_Gram_Schmidt_two():
    v1 = np.array([[0,0,4.7],[1,0,0]])
    v2 = np.array([[1,2,3],[0,1,0]])
    e1, e2 = Gram_Schmidt_two(v1,v2)
    print('e1 =', e1)
    print('e2 =', e2)
    print('result from sympy:')
    print(GramSchmidt([Matrix([0,0,4.7]), Matrix([1,2,3])], True))
    print(GramSchmidt([Matrix([1,0,0]), Matrix([0,1,0])], True))
    
def test_Gram_Schmidt_two_1D():
    v1 = np.array([0,0,4.7])
    v2 = np.array([1,2,3])
    e1, e2 = Gram_Schmidt_two(v1,v2)
    print('e1 =', e1)
    print('e2 =', e2)
    print('result from sympy:')
    print(GramSchmidt([Matrix([0,0,4.7]), Matrix([1,2,3])], True))
    

def test_uniformity_evaluation_projection():
    points = np.array([[1., 1., 2.],[2., 4., 6.]])
    v1 = np.array([[4, -1, 0], [0, 1, -22/24]])
    v2 = np.array([[0, 7/8, -1], [-1, 0, 8/24]])
    print(evaluate_uniformity_projection(points, g, v1, v2))
    print("exact answer =", [0,0])

#test_orthonormality(W)
#print()
#test_evaluate_uniformity_and_orthogonal_complement(f, point, W)
#print()
#test_compatibility_with_integral_of_motion()
#print()
#test_normalize_vector()
#print()
#test_gradient()
#test_Gram_Schmidt_two()
#print()
#test_Gram_Schmidt_two_1D()
#print()
test_grad_multi()
#print()
#test_uniformity_evaluation_projection()