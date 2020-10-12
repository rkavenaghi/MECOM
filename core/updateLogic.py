from functools import wraps
from numpy import zeros


def graphUpdateLogic(function):
    @wraps(function)
    def updateNodeLogic(self, *args, **kwargs):
        if 'node_list' not in kwargs:
            node_list = [self]
            node = self
            list_count = 0
            kwargs.update({'list_count': list_count})
            kwargs.update({'node_list': node_list})
        else:
            node_list = kwargs['node_list']
            list_count = kwargs['list_count'] + 1

            kwargs.update({'list_count': list_count})
            node = node_list[list_count]
        _list_size = len(node_list)

        for socket in node.outputs:
            if socket.hasEdges():
                for edge in socket.edges:
                    if edge.end_socket.node not in node_list:

                        node_list.append(edge.end_socket.node)

        if node != node_list[-1]:
            kwargs.update({'node_list': node_list})
            return updateNodeLogic(self, *args, **kwargs)

        updateMatrizOrder = len(node_list)
        M = zeros((updateMatrizOrder, updateMatrizOrder))

        for row, node in enumerate(node_list):
            for socket in node.outputs:
                if socket.hasEdges():
                    for edge in socket.edges:
                        M[row, node_list.index(edge.end_socket.node)] = 1

        node_sortedlist = nodeUpdateOrder(node_list, M)
        for node in node_sortedlist:
            node.refresh()

    return updateNodeLogic


def nodeUpdateOrder(node_list, connectionMatrix):
    # varre matriz de cima para baixo

    for rows in range(1, connectionMatrix.shape[0]):
        if list_score(connectionMatrix[rows]) > list_score(connectionMatrix[rows - 1]):
            # copy é utiizado pois numpy[rows,:] nao funciona adequamente

            connectionMatrix[rows - 1, :], connectionMatrix[rows, :] = connectionMatrix[rows, :], connectionMatrix[
                                                                                                  rows - 1, :].copy()
            connectionMatrix[:, rows - 1], connectionMatrix[:, rows] = connectionMatrix[:, rows], connectionMatrix[:,
                                                                                                  rows - 1].copy()
            node_list[rows], node_list[rows - 1] = node_list[rows - 1], node_list[rows]
            return nodeUpdateOrder(node_list, connectionMatrix)
    return node_list


def list_score(list_object):
    soma = sum([val * 2 ** (len(list_object) - index - 1) for index, val in enumerate(list_object)])
    return soma
