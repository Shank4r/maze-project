class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.neighbours = []

    def getNeighbours(self):
        return self.neighbours

    def get_col(self):
        return self.col

    def get_row(self):
        return self.row

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def setNeighbours(self, neighbourNodes):
        for node in neighbourNodes:
            self.neighbours.append(node)