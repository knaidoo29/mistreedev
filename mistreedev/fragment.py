import numpy as np

def id2groups(groupID):
    """Returns a list of points in each groups and the ungrouped points.

    Parameters
    ----------
    groupID : array
        Group identification number for each point or edge, -1 means the point is not a member of any group.

    Returns
    -------
    groups : array
        A 2 dimensional array object containing the member points or edges in each group.
    ungrouped : array
        A list of ungrouped points or edges.
    """
    Ngroup = int(groupID.max()) + 1
    ungrouped = []
    groups = [[] for i in range(0, Ngroup)]
    for i in range(0, len(groupID)):
        if groupID[i] != -1.:
            groups[int(groupID[i])].append(i)
        else:
            ungrouped.append(i)
    groups = np.array([np.array(groups[i]) for i in range(0, len(groups))], dtype=object)
    ungrouped = np.array(ungrouped)
    return groups, ungrouped


class Fragment:


    def __init__(self):
        """Initialises the class."""
        self.Npoint = None
        self.l = None
        self.l_index = None
        self.l_min = None
        self.l_max = None


    def set_tree(self, Npoint, l, l_index):
        """Sets the tree which we will be fragmenting into different structures.

        Parameters
        ----------
        Npoint : int
            Number of nodes in the tree.
        l : array
            The length of edges int he tree.
        l_index : array
            Two dimensional array containing the index of the points each edge is attached to.
        """
        assert type(Npoint) == np.int, 'Npart must be an integer.'
        assert len(l) == len(l_index[0]), 'Length of the edges array l must be the same as the edges index array l_index[0].'
        self.Npoint = Npoint
        self.l = l
        self.l_index = l_index
        self.l_min = l.min()
        self.l_max = l.max()


    def get_groupID(self, min_linking_length, max_linking_length, groupID=None, edgeID=None):
        """Groups points in a tree with linking edges between min_linking_length and max_linking_length.

        Parameters
        ----------
        min_linking_length : float
            Minimum linking length.
        max_linking_length : float
            Maximum linking length.
        groupID : array
            Supply the groupID from a previous run to continue group finding.
        edgeID : array
            Supply the groupID for each edge.

        Returns
        -------
        groupID : array
            Group identification number for each point, -1 means the point is not a member of any group.
        edgeID : array
            Group identification number for each edge, -1 means the edge is not a member of any group.
        """
        # check min and maximum linking length are sensible.
        assert min_linking_length < max_linking_length, 'Minimum linking length is larger than maximum linking length.'
        if min_linking_length < self.l_min:
            assert max_linking_length < self.l_max, 'Current min_linking_length and max_linking_length leave the tree unchanged.'
        # sort edges from smallest to largest keeping track of the indexs.
        which_l = np.arange(len(self.l))
        sorted_l = np.array(sorted(zip(self.l, which_l)))
        sorted_l_val = sorted_l[:, 0]
        sorted_l_ind = sorted_l[:, 1].astype('int')
        # create arrays to keep track of what points have been used and what
        # group they belong to, when groupID = 0 means the point does not
        # belong to a group.
        if groupID is None:
            groupID = np.zeros(self.Npoint)
            edgeID = np.zeros(len(self.l))
            # to keep track of the number of groups identified.
            N_groups = 0
        else:
            assert groupID is not None and edgeID is not None, 'Both groupID and edgeID must be supplied.'
            assert self.Npoint == len(groupID), 'Length of which_group is incompatible with the Tree.'
            groupID = np.copy(groupID) + 1.
            edgeID = np.copy(edgeID) + 1.
            # to keep track of the number of groups identified.
            N_groups = int(groupID.max())
        # sets the range in the sorted_l_val for which groups will be found.
        condition = np.where(self.l < min_linking_length)[0]
        start = len(condition)
        condition = np.where(self.l < max_linking_length)[0]
        end = len(condition)
        for i in range(start, end):
            # get the index of the points on either end of each edge.
            point_ind1 = self.l_index[0][sorted_l_ind[i]]
            point_ind2 = self.l_index[1][sorted_l_ind[i]]
            # check if the points are in a group
            if groupID[point_ind1] == 0. and groupID[point_ind2] == 0.:
                # both points are not in a group so we create a new group with
                # these two points
                N_groups += 1
                groupID[point_ind1] = N_groups
                groupID[point_ind2] = N_groups
                edgeID[sorted_l_ind[i]] = N_groups
            else:
                # one of both point are in a group.
                if groupID[point_ind1] != 0. and groupID[point_ind2] == 0.:
                    # point 1 is in a group but point 2 is not so we assign point 2
                    # to the same group as point 1
                    groupID[point_ind2] = groupID[point_ind1]
                    edgeID[sorted_l_ind[i]] = groupID[point_ind1]
                elif groupID[point_ind1] == 0. and groupID[point_ind2] != 0.:
                    # ditto to above but in reverse.
                    groupID[point_ind1] = groupID[point_ind2]
                    edgeID[sorted_l_ind[i]] = groupID[point_ind2]
                else:
                    if groupID[point_ind1] != 0. and groupID[point_ind2] != 0.:
                        # both points are already in groups, so we must merge the groups
                        # they are in. We merge by assigning them the smallest group value.
                        # Note: bottlenecks are going to occur here, everything before is
                        # deterministic and does not require going through the entire array.
                        if groupID[point_ind1] < groupID[point_ind2]:
                            # if point 1 is a member of a smaller valued group
                            # we set all points with point 2's group to point 1's group
                            assign_index = groupID[point_ind1]
                            not_assign_index = groupID[point_ind2]
                            condition = np.where(groupID == groupID[point_ind2])[0]
                            conditionl = np.where(edgeID == groupID[point_ind2])[0]
                        else:
                            # ditto to above but in reverse.
                            assign_index = groupID[point_ind2]
                            not_assign_index = groupID[point_ind1]
                            condition = np.where(groupID == groupID[point_ind1])[0]
                            conditionl = np.where(edgeID == groupID[point_ind1])[0]
                        groupID[condition] = assign_index
                        edgeID[conditionl] = assign_index
                        # our groups now have a missing group value, to rectify this we subtract
                        # all groups above the missing group by 1.
                        condition = np.where(groupID > not_assign_index)[0]
                        groupID[condition] -= 1.
                        condition = np.where(edgeID > not_assign_index)[0]
                        edgeID[condition] -= 1.
                        N_groups -= 1
        groupID -= 1.
        edgeID -= 1.
        return groupID, edgeID


    def clean(self):
        """Reinitialises the class and resets the class parameters."""
        self.__init__()
