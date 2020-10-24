import numpy as np


def find_friends(Npoints, edge_index):
    """Returns the 'friends' or the other points each point is connected to.

    Parameters
    ----------
    Npoints : int
        The Number of points in the Tree.
    edge_index : array
        A 2 dimensional array containing the edges of the tree.

    Returns
    -------
    friends : list
        Points connected to each point in the tree.
    """
    # check Npoints is an integer
    assert isinstance(Npoints, int), 'Npoints must be an integer.'
    # create a list of empty list with the same size as the number of points
    friends = [[] for i in range(0, Npoints)]
    # append friends for each point
    for i in range(0, len(edge_index[0])):
        friends[edge_index[0][i]].append(edge_index[1][i])
        friends[edge_index[1][i]].append(edge_index[0][i])
    return friends

def friends2groups(friends):
    """Converts a list of friends for each point to a list of groups.

    Parameters
    ----------
    friends : list
        Points connected to each point in the tree.

    Returns
    -------
    groups : list
        A list of member points in each group.
    """
    friend_count = [float(len(friends[i])) for i in range(0, len(friends))]
    mask = np.zeros(len(friends))
    groups = []
    for i in range(0, len(friends)):
        if mask[i] == 0. and friend_count[i] != 0.:
            group = np.concatenate([np.array([i]), np.array(friends[i])])
            subgroup = np.unique(np.hstack(np.array([friends[group[j]] for j in range(0, len(group))])))
            newgroup = np.unique(np.concatenate([group, subgroup]))
            while len(group) < len(newgroup):
                group = newgroup
                subgroup = np.unique(np.hstack(np.array([friends[group[j]] for j in range(0, len(group))])))
                newgroup = np.unique(np.concatenate([group, subgroup]))
            groups.append(newgroup)
            mask[group] = 1.
    return groups

def get_group_mean(groups, param, weights=None):
    """Determines the mean of `param` for each group.

    Parameters
    ----------
    groups : list
        A list of member points in each group.
    param : array
        Parameter value for each point in the tree.
    weights : array
        Weights for each point, to calculate the parameter weighted mean for each group.

    Returns
    -------
    group_param_mean : list
        Parameter mean for each group.
    """
    if weights is None:
        group_param_mean = [np.mean(param[groups[i]]) for i in range(0, len(groups))]
    else:
        group_param_mean = [np.sum(param[groups[i]]*weights[groups[i]])/np.sum(weights[groups[i]]) for i in range(0, len(groups))]
    return group_param_mean

def get_friends_in_groups(friends, groups):
    """Returns the friends of every member of every group.

    Parameters
    ----------
    friends : list
        Points connected to each point in the tree.
    groups : list
        A list of member points in each group.

    Returns
    -------
    friends_in_group : list
        List the friends of each group member in every group.
    """
    friends_in_groups = [[friends[groups[j][i]] for i in range(0, len(groups[j]))] for j in range(0, len(groups))]
    friends_in_groups = [[np.array(friends_in_groups[j][i])[friends_in_groups[j][i] > groups[j][i]] for i in range(0, len(groups[j]))] for j in range(0, len(groups))]
    return friends_in_groups

def get_group_edges(groups, friends_in_groups):
    """Returns the edges in each group

    Parameters
    ----------
    groups : list
        A list of member points in each group.
    friends_in_group : list
        List the friends of each group member in every group.

    Returns
    -------
    edge_end1 : list
        The starting point of each edge in the groups.
    edge_end2 : list
        The end points of each edge in the groups.
    """
    edge_end1 = [[groups[j][i] for i in range(0, len(groups[j])) if len(friends_in_groups[j][i]) > 0] for j in range(0, len(groups))]
    edge_end2 = [[friends_in_groups[j][i].tolist() for i in range(0, len(groups[j])) if len(friends_in_groups[j][i]) > 0] for j in range(0, len(groups))]
    return edge_end1, edge_end2
