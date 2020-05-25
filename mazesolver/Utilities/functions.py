from Utilities.Node import Node


def alreadyInList(nodesWithoutNeighbours, node1):
    for node in nodesWithoutNeighbours:
        if node.get_row() == node1.get_row() and node.get_col() == node1.get_col():
            return True
    return False


def checkTwoNodes(map, node1, node2):
    length = 0
    cost = -1
    if node1.get_col() == node2.get_col():
        cost = abs(node1.get_row() - node2.get_row())
        for row in range(node1.get_row(), node2.get_row()):
            if map[row + 1][node1.get_col()] != "X":
                if isinstance(map[row + 1][node1.get_col()], Node) and map[row + 1][node1.get_col()] is not node2:
                    break
                length += 1
            else:
                break

    if node1.get_row() == node2.get_row():
        cost = abs(node1.get_col()-node2.get_col())
        for col in range(node1.get_col(), node2.get_col()):
            if map[node1.get_row()][col + 1] != "X":
                if isinstance(map[node1.get_row()][col + 1], Node) and map[node1.get_row()][col + 1] is not node2:
                    break
                length += 1
            else:
                break

    if length == cost:
        node1.add_neighbour((node2, cost))
        node2.add_neighbour((node1, cost))


def getCloseNodes(nodeList, map, currentNode):
    neighbourNodes = []
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()
    for node in nodeList:
        length = 0
        cost = -1

        if current_col == node.get_col():
            cost = abs(node.get_row() - current_row)
            for row in range(node.get_row(), current_row):
                if map[row + 1][current_col] != "X":
                    if isinstance(map[row + 1][current_col], Node) and map[row + 1][current_col] is not currentNode:
                        break
                    length += 1
                else:
                    break

        if current_row == node.get_row():
            cost = abs(node.get_col() - current_col)
            for col in range(node.get_col(), current_col):
                if map[current_row][col + 1] != "X":
                    if isinstance(map[current_row][col + 1], Node) and map[current_row][col + 1] is not currentNode:
                        break
                    length += 1
                else:
                    break

        if length == cost:
            neighbourNodes.append((node, cost))
            node.add_neighbour((currentNode, cost))

    return neighbourNodes


def isAlreadyVisited(visitedList, row, col):
    if (row, col) in visitedList:
        return True
    return False


def isBorder(map, row, col):
    if 0 in (row, col) or len(map) - 1 in (row, col):
        return True
    return False


def getNeighbours(map, row, col):
    potentialNeighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    actualNeighbours = []
    for neighbour in potentialNeighbours:
        try:
            if -1 in neighbour or map[neighbour[0]][neighbour[1]] == "X":
                continue
            actualNeighbours.append(neighbour)

        except (ValueError, IndexError):
            continue

    return actualNeighbours


def readMaze(maze):
    map = maze["map"]
    start = maze["startingPosition"]
    end = maze["endingPosition"]

    alreadyVisited = []
    nodeList = []
    nodesWithoutNeighbours = []

    alreadyVisited.append((start[0], start[1]))
    alreadyVisited.append((end[0], end[1]))

    map[start[0]][start[1]] = Node(start[0], start[1])
    nodeList.append(map[start[0]][start[1]])

    map[end[0]][end[1]] = Node(end[0], end[1])
    nodeList.append(map[end[0]][end[1]])

    for row in range(len(map)):
        for col in range(len(map[row])):

            currentPosition = map[row][col]
            if currentPosition == "X" or isinstance(currentPosition, Node):
                continue
            alreadyVisited.append((row, col))
            neighbours = getNeighbours(map, row, col)

            if isBorder(map, row, col):
                neighbourList = [neighbour for neighbour in neighbours if not isBorder(map, neighbour[0], neighbour[1])]

                if len(neighbourList) >= 1:
                    map[row][col] = Node(row, col)

            if not isBorder(map, row, col):
                neighbourList = [neighbour for neighbour in neighbours if
                                 not isAlreadyVisited(alreadyVisited, neighbour[0], neighbour[1])]

                if len(neighbourList) >= 2:
                    map[row][col] = Node(row, col)

            currentPosition = map[row][col]
            if isinstance(currentPosition, Node) and len(nodeList) > 0:
                neighbourNodes = getCloseNodes(nodeList, map, currentPosition)

                if len(neighbourNodes) > 0:
                    currentPosition.setNeighbours(neighbourNodes)
                    nodeList.append(currentPosition)
                else:
                    supportNodes = checkSupportNodes(map, currentPosition)
                    for node in supportNodes:
                        if alreadyInList(nodesWithoutNeighbours, node):
                            continue
                        checkTwoNodes(map, currentPosition, node)
                        nodesWithoutNeighbours.append(node)
                    nodeList.append(currentPosition)


def checkSupportNodes(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()
    currentPosition = []

    if isBorder(map, current_row, current_col):
        rightNode = checkRight(map, currentNode)
        if rightNode:
            currentPosition.append(rightNode)
        downNode = checkDown(map, currentNode)
        if downNode:
            currentPosition.append(downNode)

    else:
        leftNode = checkLeft(map, currentNode)
        if leftNode:
            currentPosition.append(leftNode)
        upNode = checkUp(map, currentNode)
        if upNode:
            currentPosition.append(upNode)
        rightNode = checkRight(map, currentNode)
        if rightNode:
            currentPosition.append(rightNode)
        downNode = checkDown(map, currentNode)
        if downNode:
            currentPosition.append(downNode)

    return currentPosition


def checkLeft(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for col in range(current_col, 0, -1):
        if map[current_row][col - 1] == "X":
            break
    if col != current_col:
        return Node(current_row, col)


def checkUp(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for row in range(current_row, 0, -1):
        if map[row - 1][current_col] == "X":
            break
    if row != current_row:
        return Node(row, current_col)


def checkRight(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for col in range(current_col, len(map[currentNode.get_row()])):
        try:
            if map[current_row][col + 1] == "X":
                break
        except (ValueError, IndexError):
            break
    if col != current_col:
        return Node(current_row, col)


def checkDown(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for row in range(current_row, len(map)):
        try:
            if map[row + 1][current_col] == "X":
                break
        except (ValueError, IndexError):
            break
    if row != current_row:
        return Node(row, current_col)
