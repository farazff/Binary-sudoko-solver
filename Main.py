import math

import CSP
from CSP import *
from Variable import Variable
from Graphics import Graphics

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
    equalZeroOne(n, variables)
    moreThanTwoSame(n, variables)

    # for i in variables:
    #     print(i.getName(), " !! ", i.getDomain())
    # for var in variables[1].getDomain():
    #     res = [int(i) for i in bin(var)[2:]]
    #     while len(res) < n:
    #         res.insert(0, 0)
    #     print(res)

    # print(variables[1].getDomain())

    A = backtrackingCSP({}, variables, n, board)

    for var in A:
        res = [int(i) for i in bin(A[var])[2:]]
        while len(res) < n:
            res.insert(0, 0)
        print(var, " ", res)
    # tablesList=list(deepcopy(CSP.TablesList)).reverse()
    tables=[]
    steps=[]
    for i in CSP.TablesList:
        tables.append(i[0])
        steps.append(i[1])
    tables.reverse()
    steps.reverse()
    for i in range(len(tables)):
        print(steps[i])
        print(tables[i])


    graphics=Graphics(tables,steps,n)
    graphics.display()


if __name__ == "__main__":
    main()
