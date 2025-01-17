"""
NAME:
    sampleV_on_set
PURPOSE:
    Sample velocity of a set of points in a density function by using
    interpolation of a grid, thereby improving the efficiency of sampleV.
    
HISTORY:
    2018-06-11 - Written - Samuel Wong
"""
import numpy as np
from scipy.interpolate import RectBivariateSpline as interpolation

def separate_outliers(data, num_std):
    """
    NAME:
        separate_outliers

    PURPOSE:
        Given a numpy array of 2 dimensional tuples, separate the data to
        a group of normal points and another group of outliers whose values
        are <std> standard deviation away from the mean, in either directions.

    INPUT:
        data = a numpy array of shape (n, 2), where n is any integer
        num_std = the number of standard deviation to eliminate. Must be integer

    OUTPUT:
        (normal, outliers) = a split of the original data into two groups

    HISTORY:
        2018-06-12 - Written - Samuel Wong
    """
    # get the standard deviation and mean of x and y
    std_x, std_y = np.std(data, axis = 0)
    mean_x, mean_y = np.mean(data, axis = 0)
    # create a boolean mask that encodes which stars are outliers
    mask = np.any([np.abs(data[:, 0] - mean_x) > num_std*std_x, 
                   np.abs(data[:, 1] - mean_y) > num_std*std_y], axis = 0)
    # create outliers and normal numpy array
    outliers = data[mask]
    normal = data[~mask]
    return normal, outliers


def generate_grid(data, x_number, y_number):
    """
    NAME:
        generate_grid

    PURPOSE:
        Given a numpy array of 2 dimensional tuples, as well as the number of 
        spacing in the x and y axis of the grid, generate a grid whose
        minimum and maximum of both x and y correspond to that of the data,
        such that the grid encloses the data.

    INPUT:
        data = a numpy array of shape (n, 2), where n is any integer
        x_number = number of spacing in the x axis of the grid
        y_number = number of spacing in the y axis of the grid

    OUTPUT:
        (grid, x, y) where
        grid = an array that stores the 2 dimensional coordinate in a 2
        dimensional array
        x = the linspace in the x direction
        y = the linspace in the y direction

    HISTORY:
        2018-06-12 - Written - Samuel Wong
    """
    # get the minimum and maximum of each coordinate
    x_min, y_min = np.min(data, axis = 0)
    x_max, y_max = np.max(data, axis = 0)
    # create the linspace in each direction according to the specified number
    # of points in each axis
    x = np.linspace(x_min, x_max, x_number)
    y = np.linspace(y_min, y_max, y_number)
    # mesh and create the grid
    xv, yv = np.meshgrid(x, y)
    grid = np.dstack((xv, yv))
    return grid, x, y
    

def optimize_grid_dim(data):
    # get the minimum and maximum of each coordinate
    x_min, y_min = np.min(data, axis = 0)
    x_max, y_max = np.max(data, axis = 0)
    # get the range in each direction
    x_range = x_max - x_min
    y_range = y_max - y_min
    # get the optimized pixel in each direction that makes sure the error is
    # below a maximum error and runs in the fastest time
    x_pixel, y_pixel = get_pixel()
    # calculate the number of spacing in each direction
    x_number = int(x_range/x_pixel)
    y_number = int(y_range/y_pixel)
    return (x_number, y_number)

def get_pixel():
    return (0.3,0.3)

def sampleV_on_set(rz_set, df):
    """
    NAME:
        sampleV_on_set

    PURPOSE:
        Given a three dimensional density function (df), as well as a set of 
        r and z coordinates of stars, return three sampled velocity for each
        star.

    INPUT:
        rz_set = a numpy array containing a list of (r,z) coordinate; assumed
                 to be all in natural unit
        df = a galpy three dimensional density function

    OUTPUT:
        coord_v = a numpy array containing the original coordinate but
                        with velocity attached. Each coordinate is of the form
                        (r, z, vR, vT, vz)

    HISTORY:
        2018-06-11 - Written - Samuel Wong
    """
    # define the number of time the code repeatedly sample velocity on the grid
    # before finding the average and interpolate those values
    repeat = 1
    # separate the coodinates into outliers and normal points.
    # outliers are defined to be values more than 2 standard deviation
    normal, outliers = separate_outliers(rz_set, 10)
    
    # initialize numpy array storing result of outliers
    outlier_coord_v = np.empty((outliers.shape[0], 5))
    # sample the velocity of outliers directly
    for i, outlier in enumerate(outliers):
        R, z = outlier
        vR, vT, vz = df.sampleV(R, z)[0]
        outlier_coord_v[i] = np.array([R, z, vR, vT, vz])
    
    # for the normal stars, we will be evaluating sample v on a grid and doing
    # interpolation on it
    # initialize numpy array storing result of normal points
    normal_coord_v = np.empty((normal.shape[0], 5))
    # optimize the dimensions of the grid
    R_number, z_number = optimize_grid_dim(normal)
    # get grid
    grid, R_linspace, z_linspace = generate_grid(normal, R_number, z_number)
    # initialize grid values. We have a separate grid for each velocity value
    # grid is a 3 dimensional array since it stores pairs of values, but 
    # grid values are 2 dimensinal array
    grid_vR = np.empty((grid.shape[0], grid.shape[1]))
    grid_vT = np.empty((grid.shape[0], grid.shape[1]))
    grid_vz = np.empty((grid.shape[0], grid.shape[1]))
    # get the grid value using sample V
    # common misconception: even though we are thinking of the Rz grid as a 
    # cartesian grid, the notation in numpy has the row first and then the 
    # column. So the for loop should loop through z, then R.
    for i in range(z_number):
        for j in range(R_number):
            R, z = grid[i][j]
            # initialize array to store multiple samples of velocity
            vR = np.empty(repeat)
            vT = np.empty(repeat)
            vz = np.empty(repeat)
            for k in range(repeat):
                vR[k], vT[k], vz[k] = df.sampleV(R, z)[0]
            # store the average of the vT and the fiist sample of vR and vz on
            # grid
            grid_vR[i][j] = vR[0]
            grid_vT[i][j] = np.mean(vT)
            grid_vz[i][j] = vz[0]
    # generate interpolation objects
    ip_vR = interpolation(z_linspace, R_linspace, grid_vR)
    ip_vT = interpolation(z_linspace, R_linspace, grid_vT)
    ip_vz = interpolation(z_linspace, R_linspace, grid_vz)
    #break down normal into its R and z components
    normal_R = normal[:,0]
    normal_z = normal[:,1]
    # sample the velocity of normal points using interpolation of the grid
    # randomnize the sign of vR and vz
    n = np.size(normal_R)
    normal_vR = ip_vR.ev(normal_z, normal_R)*np.random.choice([-1,1], size = n)
    normal_vT = ip_vT.ev(normal_z, normal_R)
    normal_vz = ip_vz.ev(normal_z, normal_R)*np.random.choice([-1,1], size = n)
    print('----------------------------evaluated all interpolation')
    # putting together position coordinate with velocity coordinate for normal
    # points
    normal_coord_v = np.dstack((normal_R, normal_z, normal_vR, 
                                     normal_vT, normal_vz))[0]
    
    # combine normal and outlier result
    coord_v = np.vstack((normal_coord_v, outlier_coord_v))
    return coord_v
    