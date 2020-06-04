class Nodelist:
    def __init__(self):
        self.list = []

    def get_list(self):
        return self.list

    def set_list(self, newList):
        self.list = newList

    def get_start(self):
        return self.list[0]

    def get_end(self):
        return self.list[1]

    def get_currentPos(self, currentPos):
        for node in self.list:
            if node.get_col() == currentPos[0] and node.get_row() == currentPos[1]:
                return node
