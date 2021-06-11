import math
from copy import deepcopy

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


def makeRowNodeConsistent(n, board, variables):
    for rowNUM in range(n):
        tempList = []
        for domainVar in variables[rowNUM].getDomain():
            res = [int(i) for i in bin(domainVar)[2:]]
            while len(res) < n:
                res.insert(0, 0)
            isOK = True
            for k in range(n):
                if board[rowNUM][k] != '-':
                    if str(board[rowNUM][k]) != str(res[k]):
                        isOK = False
                        break

            if isOK is True:
                tempList.append(deepcopy(domainVar))

        variables[rowNUM].setDomain(tempList)


def makeColNodeConsistent(n, board, variables):
    for colNUM in range(n):
        tempList = []
        for domainVar in variables[n + colNUM].getDomain():
            res = [int(i) for i in bin(domainVar)[2:]]
            while len(res) < n:
                res.insert(0, 0)
            isOK = True
            for k in range(n):
                if board[k][colNUM] != '-':
                    if str(board[k][colNUM]) != str(res[k]):
                        isOK = False
                        break

            if isOK is True:
                tempList.append(deepcopy(domainVar))

        variables[n + colNUM].setDomain(tempList)


def main():
    size = input().split()
    n = int(size[0])
    board = []
    for i in range(n):
        temp = input()
        row = temp.split()
        board.append(row)

    variables = []
    createVariables(n, variables)
    makeDomainFull(n, variables)
    makeRowNodeConsistent(n, board, variables)
    makeColNodeConsistent(n, board, variables)
    # print(variables[7].getDomain())


if __name__ == "__main__":
    main()
