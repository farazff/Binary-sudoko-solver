import math
from copy import deepcopy

from CSP import getTablesList, backtrackingCSP, makeColNodeConsistent, makeRowNodeConsistent
from Graphics import Graphics
from Variable import Variable


def createVariables(n, variables):
    for i in range(n):
        variables.append(Variable("R" + str(i)))
    for i in range(n):
        variables.append(Variable("C" + str(i)))


def makeDomainFull(n, variables):
    for variable in variables:
        for num in range(int(math.pow(2, n))):
            variable.addDomain(num)


def equalZeroOne(n, variables):
    for varNUM in range(2 * n):
        tempList = []
        for domainVar in variables[varNUM].getDomain():
            res = [int(i) for i in bin(domainVar)[2:]]
            while len(res) < n:
                res.insert(0, 0)
            ZC = OC = int(0)
            for i in res:
                if str(i) == '0':
                    ZC += 1
                if str(i) == '1':
                    OC += 1
            if ZC == OC:
                tempList.append(deepcopy(domainVar))

        variables[varNUM].setDomain(tempList)


def moreThanTwoSame(n, variables):
    for varNUM in range(2 * n):
        tempList = []
        for domainVar in variables[varNUM].getDomain():
            res = [int(i) for i in bin(domainVar)[2:]]
            while len(res) < n:
                res.insert(0, 0)
            isOk = True

            for i in range(0, n - 2):
                if res[i] == res[i + 1] and res[i + 1] == res[i + 2]:
                    isOk = False
                    break

            if isOk:
                tempList.append(deepcopy(domainVar))

        variables[varNUM].setDomain(tempList)


def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=" ")
        print()
    print(end="\n")


def start(tesNum):
    path = "Puzzles/puzzle" + str(tesNum) + ".txt"
    f = open(path, "r")
    firstLineSTR = f.readline()
    firstLineLIST = firstLineSTR.split()
    n = int(firstLineLIST[0])
    board = []
    for i in range(n):
        temp = f.readline()
        row = temp.split()
        board.append(row)

    saveBoard = deepcopy(board)
    printBoard(board, n)
    variables = []
    createVariables(n, variables)
    makeDomainFull(n, variables)
    makeRowNodeConsistent(n, board, variables)
    makeColNodeConsistent(n, board, variables)
    equalZeroOne(n, variables)
    moreThanTwoSame(n, variables)

    A = backtrackingCSP({}, variables, n, board)

    if type(A) is bool:
        print("There is no answer you looser :)")
    else:
        for var in A:
            res = [int(i) for i in bin(A[var])[2:]]
            while len(res) < n:
                res.insert(0, 0)
            print(var, " ", A[var])

        for i in getTablesList():
            print(i[1])
            printBoard(i[0], n)

    tables = []
    steps = []
    for i in getTablesList():
        tables.append(i[0])
        steps.append(i[1])
    tables.append(saveBoard)
    steps.append("n0")
    tables.reverse()
    steps.reverse()
    graphic = Graphics(tables, steps, n)
    graphic.display()
