import numpy as np


def dist_from_line(x0, y0, z0, x1, y1, z1, xr, yr, zr):
    """ Finds the perpendicular and parallel distance from a line, not the distance
    from the line is given in units of the lines length.

    Parameters
    ----------
    x0, y0, z0 : float
        The coordinate of one end of the line.
    x1, y1, z1 : float
        The coordinate of the other end of the line.
    xr, yr, zr : array_like
        The points we wish to check the distance to the line.

    Returns
    -------
    dist_para : array_like
        The distance of points parallel to the line given in units of the of the
        lines length.
    dist_perp : array_like
        The distance of points perpendicular to the line.
    """
    a = x1 - x0
    b = y1 - y0
    c = z1 - z0
    dist_para = a*(xr - x0) + b*(yr - y0) + c*(zr - z0)
    dist_para /= a**2. + b**2. + c**2.
    xnew = a*dist_para + x0
    ynew = b*dist_para + y0
    znew = c*dist_para + z0
    dist_perp = np.sqrt((xr-xnew)**2. + (yr-ynew)**2. + (zr-znew)**2.)
    return dist_para, dist_perp


def count_in_cylinder(dist_para, dist_perp, rmax):
    """ Counts the number of points in a cylinders, i.e. a distance rmax from a line.

    Parameters
    ----------
    dist_para : array_like
        The parallel distance from a line.
    dist_perp : array_like
        The perpendicular distance from a line.
    rmax : float/array_like
        The radius of the cylinder or radiuses of cylinders if input is an array.

    Returns
    -------
    counts : float/array_like
        Number of points within a cylinder or if rmax is an array then the number
        of points in each cylinder.
    """
    condition1 = np.where((dist_para >= 0.) & (dist_para <= 1.))[0]
    if np.isscalar(rmax) is True:
        condition2 = np.where(dist_perp[condition1] <= rmax)[0]
        counts = float(len(condition2))
    else:
        _bin_edges = np.concatenate([np.array([0.]), np.array(sorted(rmax))])
        counts, bin_edges = np.histogram(dist_perp[condition1], bins=_bin_edges, normed=False)
        counts = np.cumsum(counts)
    return counts
