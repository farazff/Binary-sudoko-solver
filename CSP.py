import random
from copy import deepcopy

from Main import makeRowNodeConsistent, makeColNodeConsistent


def completenessChecker(A, n):
    if len(A) == 2 * n:
        return True
    return False


def isThereEmptyVariable(varDomains):
    for i in varDomains:
        if i.getDomainLen() == 0:
            return True
    return False


def MCV(A, varDomain):
    tempList = []
    # print(A)
    for variable in varDomain:
        if variable.getName() not in A:
            tempList.append(variable)

    tempList.sort(key=lambda x: x.getDomainLen(), reverse=False)
    finalList = []
    for i in tempList:
        if i.getDomainLen() == tempList[0].getDomainLen():
            finalList.append(i)

    select = random.randint(0, len(finalList) - 1)
    return finalList[select]


def forwardChecking(varDomain, board, n):
    # vv = deepcopy(varDomain)
    # for i in varDomain:
    #     print("\n", i.getName(), "  :  ", i.getDomain(), end="-")
    # checking(varDomain)
    # for i in varDomain:
    #     print("\n", i.getName(), "  :::  ", i.getDomain(), end="-")
    # TODO -> rows and columns de conflicting handling

    makeRowNodeConsistent(n, board, varDomain)
    makeColNodeConsistent(n, board, varDomain)

    return varDomain


def binaryToDecimal(binary):
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def checking(varDomain):
    tmpDictR = {}
    tmpDictC = {}
    for dName in varDomain:
        if 'C' in dName.getName():
            for dom in dName.getDomain():
                try:
                    tmpDictC[dom]
                    dName.getDomain().remove(dom)
                    tmpDictC[dom] = False
                except:
                    tmpDictC[dom] = True
        elif 'R' in dName.getName():
            for dom in dName.getDomain():
                try:
                    tmpDictR[dom]
                    dName.getDomain().remove(dom)
                    tmpDictR[dom] = False
                except:
                    tmpDictR[dom] = True


def LCV(domain):
    # TODO: Complete LCV
    return domain


def updateBoard(board, name, v, n):
    res = [int(i) for i in bin(v)[2:]]
    while len(res) < n:
        res.insert(0, 0)
    if name[0] == 'R':
        rowNum = int(name[1])
        for i in range(n):
            board[rowNum][i] = res[i]
        return

    if name[0] == 'C':
        colNum = int(name[1])
        for i in range(n):
            board[i][colNum] = res[i]
        return


def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=" ")
        print()
    print(end="\n\n")


def backtrackingCSP(A, varDomains, n, board):
    if completenessChecker(A, n):
        return A

    X = MCV(A, varDomains)
    D = LCV(X.getDomain())

    for v in D:

        domain = deepcopy(varDomains)
        boardThisLevel = deepcopy(board)
        A[X.getName()] = v
        updateBoard(boardThisLevel, X.getName(), v, n)

        domain = forwardChecking(domain, boardThisLevel, n)

        if isThereEmptyVariable(domain):
            return False

        result = backtrackingCSP(A, deepcopy(domain), n, boardThisLevel)

        if result:
            printBoard(board, n)
            return result
        A.pop(X.getName())

    return False
