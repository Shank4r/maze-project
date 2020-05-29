from Utilities.Node import Node
from queue import PriorityQueue
from heapdict import heapdict
import numpy as np


def readMaze(maze):
    map = maze["map"]
    start = maze["startingPosition"]
    end = maze["endingPosition"]

    alreadyVisited = []
    nodeList = []

    alreadyVisited.append((start[0], start[1]))
    alreadyVisited.append((end[0], end[1]))

    map[start[1]][start[0]] = Node(start[1], start[0], startNode=True)
    nodeList.append(map[start[1]][start[0]])

    map[end[1]][end[0]] = Node(end[1], end[0], endNode=True)
    nodeList.append(map[end[1]][end[0]])

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

            else:

                if isCorner(map, row, col):
                    map[row][col] = Node(row, col)
                else:
                    neighbourList = [neighbour for neighbour in neighbours if
                                     not isAlreadyVisited(alreadyVisited, neighbour[0], neighbour[1])]

                    if len(neighbourList) >= 2:
                        map[row][col] = Node(row, col)

            currentPosition = map[row][col]
            if isinstance(currentPosition, Node) and len(nodeList) > 0:
                nodeList.append(currentPosition)

    uselessNodes = []
    for node in nodeList:
        nearestNodes = findNearestNodes(map, node)
        if len(nearestNodes) > 0:
            node.set_neighbours(nearestNodes)
        else:
            uselessNodes.append(node)

    for node in uselessNodes:
        nodeList.remove(node)

    return nodeList


def calculateCost(node1, node2):
    rowDiff = abs(node1.get_row() - node2.get_row())
    colDiff = abs(node1.get_col() - node2.get_col())

    if rowDiff == 0 and node1.get_col() > node2.get_col():
        return "W", colDiff
    elif rowDiff == 0 and node1.get_col() < node2.get_col():
        return "E", colDiff
    elif colDiff == 0 and node1.get_row() > node2.get_row():
        return "N", rowDiff
    elif colDiff == 0 and node1.get_row() < node2.get_row():
        return "S", rowDiff


def calculateFinalPath(finalRoute):
    finalPath = []
    for node in reversed(finalRoute):
        if node.get_parent():
            direction, cost = calculateCost(node.get_parent(), node)
            value = [direction] * cost
            finalPath.extend(value)

    return finalPath



def findShortestPath(startNode, endNode):
    candidateQueue = heapdict()
    alreadyVisited = []
    finalRoute = []
    candidateQueue[startNode] = 0

    while candidateQueue:
        currentNode = candidateQueue.popitem()[0]
        alreadyVisited.append(currentNode)
        if currentNode is endNode:
            currentNode.set_parent(finalRoute[-1])
            finalRoute.append(currentNode)
            finalPath = calculateFinalPath(finalRoute)
            finalPath.reverse()
            print("Funnet sluttnoden", currentNode)
            return finalPath

        neighbourNodes = currentNode.get_neighbours()
        for neighbour in neighbourNodes:
            currentNeighbour = neighbour[0]

            currentNeighbour.set_g(currentNode.get_g() + neighbour[1])
            currentNeighbour.set_h(endNode)
            currentNeighbour.update_f()

            if currentNeighbour not in finalRoute:
                candidateQueue[currentNeighbour] = currentNeighbour.get_f()

        alternativeNodes = [x for x in currentNode.get_neighbourNodes() if x not in finalRoute]
        nextNode = candidateQueue.peekitem()[0]

        if nextNode in currentNode.get_neighbourNodes():
            if len(finalRoute) > 0:
                currentNode.set_parent(finalRoute[-1])
            finalRoute.append(currentNode)
        elif len(alternativeNodes) > 0:
            for node in alternativeNodes:
                if node in candidateQueue:
                    continue
            candidateQueue.popitem()
            currentNode.set_parent(finalRoute[-1])
            finalRoute.append(currentNode)
        elif len(alternativeNodes) < 1:
            continue


def setHeuristic(endNode, currentNode):
    if endNode is not currentNode:
        colDiff = abs(currentNode.get_col() - endNode.get_col())
        rowDiff = abs(currentNode.get_row() - endNode.get_row())
        currentNode.set_h(colDiff ** 2 + rowDiff ** 2)
    else:
        currentNode.set_h(0)


def borderType(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    if current_row == 0 and current_col == 0:
        return "top-left-border"
    elif current_row == 0 and current_col == len(map[current_row]) - 1:
        return "top-right-border"
    elif current_row == len(map) - 1 and current_col == 0:
        return "bottom-left-border"
    elif current_row == len(map) - 1 and current_col == len(map[current_row]) - 1:
        return "bottom-right-border"

    elif current_row == 0 and current_col != 0 and current_col != len(map[current_row]) - 1:
        return "top-border"
    elif current_row == len(map) - 1 and current_col != 0 and current_col != len(map[current_row]) - 1:
        return "bottom-border"

    elif current_col == 0 and current_row != 0 and current_row != len(map) - 1:
        return "left-border"
    elif current_col == len(map) - 1 and current_row != 0 and current_row != len(map) - 1:
        return "right-border"


def findNearestNodes(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()
    nearestNodes = []

    if isBorder(map, current_row, current_col):

        border_type = borderType(map, currentNode)
        if border_type == "top-left-border":
            rightNode, cost = checkRight(map, currentNode)
            if rightNode:
                nearestNodes.append((rightNode, cost))
            downNode, cost = checkDown(map, currentNode)
            if downNode:
                nearestNodes.append((downNode, cost))

        elif border_type == "top-right-border":
            leftNode, cost = checkLeft(map, currentNode)
            if leftNode:
                nearestNodes.append((leftNode, cost))
            downNode, cost = checkDown(map, currentNode)
            if downNode:
                nearestNodes.append((downNode, cost))

        elif border_type == "bottom-left-border":
            upNode, cost = checkUp(map, currentNode)
            if upNode:
                nearestNodes.append((upNode, cost))
            rightNode, cost = checkRight(map, currentNode)
            if rightNode:
                nearestNodes.append((rightNode, cost))

        elif border_type == "bottom-right-border":
            upNode, cost = checkUp(map, currentNode)
            if upNode:
                nearestNodes.append((upNode, cost))
            leftNode, cost = checkLeft(map, currentNode)
            if leftNode:
                nearestNodes.append((leftNode, cost))

        elif border_type == "top-border":
            leftNode, cost = checkLeft(map, currentNode)
            if leftNode:
                nearestNodes.append((leftNode, cost))
            downNode, cost = checkDown(map, currentNode)
            if downNode:
                nearestNodes.append((downNode, cost))
            rightNode, cost = checkRight(map, currentNode)
            if rightNode:
                nearestNodes.append((rightNode, cost))

        elif border_type == "bottom-border":
            leftNode, cost = checkLeft(map, currentNode)
            if leftNode:
                nearestNodes.append((leftNode, cost))
            rightNode, cost = checkRight(map, currentNode)
            if rightNode:
                nearestNodes.append((rightNode, cost))
            upNode, cost = checkUp(map, currentNode)
            if upNode:
                nearestNodes.append((upNode, cost))

        elif border_type == "left-border":
            rightNode, cost = checkRight(map, currentNode)
            if rightNode:
                nearestNodes.append((rightNode, cost))
            upNode, cost = checkUp(map, currentNode)
            if upNode:
                nearestNodes.append((upNode, cost))
            downNode, cost = checkDown(map, currentNode)
            if downNode:
                nearestNodes.append((downNode, cost))

        elif border_type == "right-border":
            upNode, cost = checkUp(map, currentNode)
            if upNode:
                nearestNodes.append((upNode, cost))
            downNode, cost = checkDown(map, currentNode)
            if downNode:
                nearestNodes.append((downNode, cost))
            leftNode, cost = checkLeft(map, currentNode)
            if leftNode:
                nearestNodes.append((leftNode, cost))

    else:
        leftNode, cost = checkLeft(map, currentNode)
        if leftNode:
            nearestNodes.append((leftNode, cost))
        upNode, cost = checkUp(map, currentNode)
        if upNode:
            nearestNodes.append((upNode, cost))
        rightNode, cost = checkRight(map, currentNode)
        if rightNode:
            nearestNodes.append((rightNode, cost))
        downNode, cost = checkDown(map, currentNode)
        if downNode:
            nearestNodes.append((downNode, cost))

    return nearestNodes


def checkLeft(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for col in range(current_col, 0, -1):
        if map[current_row][col - 1] == "X":
            break
        elif isinstance(map[current_row][col - 1], Node):
            return map[current_row][col - 1], abs(col - 1 - current_col)
    return None, None


def checkUp(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for row in range(current_row, 0, -1):
        if map[row - 1][current_col] == "X":
            break
        elif isinstance(map[row - 1][current_col], Node):
            return map[row - 1][current_col], abs(row - 1 - current_row)
    return None, None


def checkRight(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for col in range(current_col, len(map[currentNode.get_row()])):
        try:
            if map[current_row][col + 1] == "X":
                break
            elif isinstance(map[current_row][col + 1], Node):
                return map[current_row][col + 1], abs(col + 1 - current_col)
        except (ValueError, IndexError):
            break
    return None, None


def checkDown(map, currentNode):
    current_row = currentNode.get_row()
    current_col = currentNode.get_col()

    for row in range(current_row, len(map)):
        try:
            if map[row + 1][current_col] == "X":
                break
            elif isinstance(map[row + 1][current_col], Node):
                return map[row + 1][current_col], abs(row + 1 - current_row)
        except (ValueError, IndexError):
            break
    return None, None


def isAlreadyVisited(visitedList, row, col):
    if (row, col) in visitedList:
        return True
    return False


def isBorder(map, row, col):
    if 0 in (row, col) or len(map) - 1 in (row, col):
        return True
    return False


def isCorner(map, row, col):
    up = (row - 1, col)
    down = (row + 1, col)
    left = (row, col - 1)
    right = (row, col + 1)

    if map[down[0]][down[1]] != "X" and map[right[0]][right[1]] != "X" and map[up[0]][up[1]] == "X" and \
            map[left[0]][
                left[1]] == "X":
        return True
    elif map[down[0]][down[1]] != "X" and map[left[0]][left[1]] != "X" and map[up[0]][up[1]] == "X" and \
            map[right[0]][
                right[1]] == "X":
        return True
    elif map[up[0]][up[1]] != "X" and map[right[0]][right[1]] != "X" and map[down[0]][down[1]] == "X" and map[left[0]][
        left[1]] == "X":
        return True
    elif map[up[0]][up[1]] != "X" and map[left[0]][left[1]] != "X" and map[down[0]][down[1]] == "X" and map[right[0]][
        right[1]] == "X":
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


# def findShortestPath(startNode, endNode):
#     route = []
#     temp_queue = PriorityQueue()
#     alreadyVisited = []
#     temp_queue.put((startNode.get_heuristic(), startNode))
#     route.append(startNode)
#     while temp_queue:
#         currentNode = temp_queue.get()[1]
#         if currentNode not in route[-1].get_neighbourNodes() and currentNode is not route[-1]:
#             continue
#         alreadyVisited.append(currentNode)
#         neighbours = currentNode.get_neighbours()
#         for currentNeighbour in neighbours:
#             total = currentNeighbour[0].get_heuristic() + currentNeighbour[1]
#             if total < currentNeighbour[0].get_totalCost():
#                 currentNeighbour[0].set_totalCost(total)
#             if currentNeighbour[0] not in alreadyVisited:
#                 temp_queue.put((currentNeighbour[0].get_totalCost(), currentNeighbour[0]))
#
#         if temp_queue.queue[0][1] in currentNode.get_neighbourNodes() and currentNode not in route:
#             route.append(currentNode)
#         elif temp_queue.queue[0][1] not in route[-1].get_neighbourNodes():
#             del route[-1]