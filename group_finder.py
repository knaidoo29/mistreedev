import numpy as np
from sklearn.neighbors import KDTree


def find_friends_2d(x, y, linking_length):
    """Finds friends for a given set of points in 2D. This is defined to be points
    that are a distance=linking_length from a points.

    Parameters
    ----------
    x, y, z : array_like
        Positions
    linking_length : float
        Linking length distance.

    Returns
    -------
    friends : list
        A list of friends for each given point.
    """
    pos = np.array([x, y]).T
    tree_data = KDTree(pos, leaf_size=10)
    friends = tree_data.query_radius(pos, r=linking_length)
    friends = [sorted(friends[i]) for i in range(0, len(friends))]
    friends = [np.array(friends[i])[np.where(np.array(friends[i]) != i)[0]] for i in range(0, len(friends))]
    return friends


def find_friends_3d(x, y, z, linking_length):
    """Finds friends for a given set of points in 3D. This is defined to be points
    that are a distance=linking_length from a points.

    Parameters
    ----------
    x, y, z : array_like
        Positions
    linking_length : float
        Linking length distance.

    Returns
    -------
    friends : list
        A list of friends for each given point.
    """
    pos = np.array([x, y, z]).T
    tree_data = KDTree(pos, leaf_size=10)
    friends = tree_data.query_radius(pos, r=linking_length)
    friends = [sorted(friends[i]) for i in range(0, len(friends))]
    friends = [np.array(friends[i])[np.where(np.array(friends[i]) != i)[0]] for i in range(0, len(friends))]
    return friends


def count_friends(friends):
    """Gets the friend counts.

    Parameters
    ----------
    friends : list
        A list of friends for each given point.

    Returns
    -------
    counts : list
        The number of 'friends' for each points.
    """
    counts = [len(friends[i]) for i in range(0, len(friends))]
    counts = np.array(counts).astype('float')
    return counts


def get_groups(friends, counts):
    """Gets groups based on friends and friend counts.

    Parameters
    ----------
    friends : list
        A list of friends for each given point.
    counts : list
        The number of 'friends' for each points.

    Returns
    -------
    groups : list
        A list of member points in each group.
    """
    _mask = np.zeros(len(friends))
    groups = []
    for j in range(0, len(friends)):
        if _mask[j] == 0. and counts[j] != 0:
            group = np.concatenate([np.array([j]), np.array(friends[j])])
            subgroup = np.unique(np.hstack(np.array([friends[group[k]] for k in range(0, len(group))])))
            newgroup = np.unique(np.concatenate([group, subgroup]))
            while len(group) < len(newgroup):
                group = newgroup
                subgroup = np.unique(np.hstack(np.array([friends[group[k]] for k in range(0, len(group))])))
                newgroup = np.unique(np.concatenate([group, subgroup]))
            groups.append(newgroup)
            _mask[group] = 1.
    groups = np.array(groups)
    return groups


def get_group_param_mean(groups, parameter):
    """Gets the mean of an input value for each group.

    Parameters
    ----------
    groups : list
        A list of member points in each group.
    parameter : array_like
        Parameter value for each point which we want the mean of for each group.

    Returns
    -------
    group_param_mean : array
        The mean parameter for each group.
    """
    group_param_mean = np.array([np.mean(parameter[groups[i]]) for i in range(0, len(groups))])
    return group_param_mean


class GroupFinder:

    """Group finder class function."""

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.mode = None
        self.linking_length = None
        self.friends = None
        self.counts = None
        self.groups = None
        self.x_group = None
        self.y_group = None
        self.z_group = None
        self.x_in = None
        self.y_in = None
        self.z_in = None
        self.x_out = None
        self.y_out = None
        self.z_out = None
        self.N_groups = None
        self.N_points_in = None
        self.N_points_out = None

    def setup(self, x, y, z=None):
        """Input positions in 2D or 3D coordinates.

        Parameters
        ----------
        x, y, z : array_like
            Positions given in 2D or 3D (=> z is optional.)
        """
        if z is None:
            self.mode = '2D'
        else:
            self.mode = '3D'
        self.x = x
        self.y = y
        self.z = z

    def find_friends(self, linking_length):
        """Find 'friends', i.e. points that are a distance 'linking_length' apart.

        Parameters
        ----------
        linking_length : float
            Linking length distance.
        """
        self.linking_length = linking_length
        if self.mode == '2D':
            self.friends = find_friends_2d(self.x, self.y, self.linking_length)
        elif self.mode == '3D':
            self.friends = find_friends_3d(self.x, self.y, self.z, self.linking_length)
        else:
            print('Mode Error:', self.mode)

    def count_friends(self):
        """Counts the number of 'friends' for each point."""
        self.counts = count_friends(self.friends)

    def get_groups(self):
        """Creates a catalogue of group members."""
        self.groups = get_groups(self.friends, self.counts)
        self.N_groups = len(self.groups)

    def get_group_pos(self):
        """Finds group mean positions."""
        self.x_group = get_group_param_mean(self.groups, self.x)
        self.y_group = get_group_param_mean(self.groups, self.y)
        if self.mode == '3D':
            self.z_group = get_group_param_mean(self.groups, self.z)

    def get_grouped(self):
        """Finds the positions of points that are group members."""
        condition = np.where(self.counts != 0.)[0]
        self.N_points_in = len(condition)
        self.x_in = self.x[condition]
        self.y_in = self.y[condition]
        if self.mode == '3D':
            self.z_in = self.z[condition]

    def get_non_grouped(self):
        """Finds the positions of points that are non group members."""
        condition = np.where(self.counts == 0.)[0]
        self.x_out = self.x[condition]
        self.y_out = self.y[condition]
        if self.mode == '3D':
            self.z_out = self.z[condition]

    def get_catalogue(self, linking_length, x, y, z=None):
        """Outputs a catalogue of group mean positions and non-grouped points.

        Parameters
        ----------
        linking_length : float
            Linking length distance.
        x, y, z : array_like
            Positions.

        Returns
        -------
        x_cat, y_cat, z_cat : array_like
            Positions of groups and non-grouped points.
        """
        self.setup(x, y, z)
        self.find_friends(linking_length)
        self.count_friends()
        self.get_groups()
        self.get_group_pos()
        self.get_non_grouped()
        x_cat = np.concatenate([self.x_group, self.x_out])
        y_cat = np.concatenate([self.y_group, self.y_out])
        if self.mode == '3D':
            z_cat = np.concatenate([self.z_group, self.z_out])
            return x_cat, y_cat, z_cat
        else:
            return x_cat, y_cat

    def clean(self):
        """Reset internal parameters."""
        self.__init__()
