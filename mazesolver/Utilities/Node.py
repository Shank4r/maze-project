from math import inf


class Node:
    def __init__(self, row, col, startNode=False, endNode=False):
        self.row = row
        self.col = col
        if startNode:
            self.g = 0
        else:
            self.g = inf
        if endNode:
            self.h = 0
        else:
            self.h = inf
        self.f = inf
        self.neighbours = []
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def get_neighbours(self):
        return self.neighbours

    def get_neighbourNodes(self):
        neighbourNodes = []
        for node in self.neighbours:
            neighbourNodes.append(node[0])
        return neighbourNodes

    def get_col(self):
        return self.col

    def get_row(self):
        return self.row

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def set_neighbours(self, neighbourNodes):
        for node in neighbourNodes:
            self.neighbours.append(node)

    def set_g(self, value):
        self.g = value

    def get_g(self):
        return self.g

    def set_h(self, endNode):
        if self is not endNode:
            colDiff = abs(self.get_col() - endNode.get_col())
            rowDiff = abs(self.get_row() - endNode.get_row())
            self.h = (colDiff ** 2) + (rowDiff ** 2)

    def get_h(self):
        return self.h

    def update_f(self):
        self.f = self.g + self.h

    def get_f(self):
        return self.f

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
