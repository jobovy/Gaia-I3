"""
NAME:
    main_program_cluster

PURPOSE:
    Evaluate uniformity of dot product on a cluster of points in phase space
    given by kmeans.
    
HISTORY:
    2018-06-20 - Written - Samuel Wong
"""
import numpy as np
import os, sys
# get the outer folder as the path
outer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
check_uniformity_path =  os.path.abspath(os.path.join(outer_path, 'check_uniformity_of_density'))
sys.path.append(outer_path)
sys.path.append(check_uniformity_path)
# import relevant functions from different folders
from check_uniformity_of_density.Integral_of_Motion import *
from check_uniformity_of_density.Linear_Algebra import *
from check_uniformity_of_density.Uniformity_Evaluation import *
from search import search_online
from search import search_local
from kde.kde_function import *
from kmeans.kmeans import *
from tools.tools import *

def evaluate_uniformity_from_point(a, density):
    """
    NAME:
        evaluate_uniformity_from_point

    PURPOSE:
        Given a density function and a point, find the gradient of energy
        and angular momentum and the density at the point, and find the normalize
        dot products between the gradient of density and four orthonormal basis
        vectors of the orthgonal complement of the gradient of energy and
        angular momentum.

    INPUT:
        a = the point in phase space with six coordinates in galactocentric
            Cartesian with natural units
        density = a differentiable density function

    OUTPUT:
        directional_derivatives = a numpy array containing the directional
                                  derivative of density along each direction
                                  of the basis vectors generating the subspace

    HISTORY:
        2018-06-20 - Written - Samuel Wong
    """
    # get the gradient of energy and momentum of the search star
    del_E = grad(Energy, 6)
    del_Lz = grad(L_z, 6)
    del_E_a = del_E(a)
    del_Lz_a = del_Lz(a)
    # create matrix of the space spanned by direction of changing energy and momentum
    V = np.array([del_E_a, del_Lz_a])
    # get the 4 dimensional orthogonal complement of del E and del Lz
    W = orthogonal_complement(V)
    # evaluate if density is changing along the subspace 
    # check to see if they are all 0; if so, it is not changing
    directional_derivatives = evaluate_uniformity(density, a, W)
    return directional_derivatives


def main(custom_density = None, search_method = "online"):
    """
    NAME:
        main

    PURPOSE:
        Call on all modules to evaluate uniformity of density on a cluster of 
        points provided by kmeans. Allows the user to specify search method to
        generate sample stars around a point in phase space. Also, allows user
        to give custom density function, but since no points are given for a
        custom density, this program only evaluates uniformity at a point when
        custom density is given.

    INPUT:
        custom_density = a customized density functiont that takes an array
                         of 6 numbers representing the coordinate and return
                         the density; if this input is None, then the code
                         will use a search method to get data from Gaia catalogue
                         and use KDE to genereate a density function
        search_method = search the gaia catalogue online ("online"),
                        locally on a downloaded file ('local'), or use the
                        the entire downloaded gaia rv file ('all of local')

    HISTORY:
        2018-06-20 - Written - Samuel Wong
    """
    file_name = input("File name to be stored: ")
    # at this point, everything should have physical units
    # get coordinate of the star to be evaluated from user
    point_galactocentric, point_galactic = get_star_coord_from_user()
    if custom_density == None:
        # define parameters for the search and KDE
        epsilon = 0.5
        v_scale = 0.1
        # depending on the argument of main function, search stars online, locally
        # or use all of local catalogue
        # if we are searching, get stars within an epsilon ball of the point in 
        # phase space from Gaia, input the galactic coordinate into search function
        if search_method == "online":
            samples = search_online.search_phase_space(*point_galactic, epsilon, v_scale)
        elif search_method == "local":
            samples = search_local.search_phase_space(*point_galactic, epsilon, v_scale)
        elif search_method == "all of local":
            samples = search_local.get_entire_catalogue()
        print('Found a sample of {} of stars,'.format(np.shape(samples)[0]))
        # Turn all data to natrual units; working with natural unit, galactocentric,
        # cartesian from this point on
        samples = to_natural_units(samples)
        # use the samples and a KDE learning method to generate a density function
        density = generate_KDE(samples, 'epanechnikov', v_scale)
    else:
        density = custom_density # use the custom density function
    
    # if custom density is given, only evaluate uniformity at given point
    if custom_density != None:
        # convert the point to natural unit first
        point_gc_natural = to_natural_units(np.array([point_galactocentric]))[0]
        directional_derivatives = evaluate_uniformity_from_point(
                point_gc_natural, density)
        for i in range(len(directional_derivatives)):
            print('del_rho dot w_{} = {}'.format(i, directional_derivatives[i]))
    else:
        # let batch size be 10% of the number of samples
        batch_size = 0.1 * np.shape(samples)[0]
        # define the number of cluster centers
        cluster_number = 1000
        # use kmenas to generate a cluster of points
        cluster = kmeans(samples, cluster_number, batch_size)
        # initialize an array of directional derivative for each point
        result = np.empty((np.shape(cluster)[0], 4))
        # evaluate uniformity for each point in cluster
        for (i, point) in enumerate(cluster):
            result[i] = evaluate_uniformity_from_point(point, density)
            print('At point {}, dot products are {}'.format(point, result[i]))
        # output summary information
        mean_of_max = np.mean(np.max(result, axis = 1))
        print('The average of the maximum dot product is ', mean_of_max)
        # save result
        np.save(file_name, result)
    
if __name__ == "__main__":
    main(None, "local")
