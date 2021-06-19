import random
from copy import deepcopy
import numpy
from Main import makeRowNodeConsistent, makeColNodeConsistent

TablesList = []


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

    for row in range(len(board)):
        if '-' not in ''.join(map(str, board[row])):
            for i in varDomain:
                if int(''.join(map(str, board[row])), 2) in i.getDomain() and 'R' in i.getName():
                    if int(i.getName()[1:]) != row:
                        i.getDomain().remove(int(''.join(map(str, board[row])), 2))

    boardR = numpy.array(board)
    boardR = boardR.T
    for column in range(len(boardR)):
        if '-' not in ''.join(map(str, boardR[column])):
            for i in varDomain:
                if int(''.join(map(str, boardR[column])), 2) in i.getDomain() and 'C' in i.getName():
                    if int(i.getName()[1:]) != column:
                        i.getDomain().remove(int(''.join(map(str, boardR[column])), 2))

    makeRowNodeConsistent(n, board, varDomain)
    makeColNodeConsistent(n, board, varDomain)

    return varDomain


def LCV(var, domain ,varDomains, board,n):

    dictForSort = {}
    for domainItem in domain:
            dictForSort[domainItem] = 0
            varDomainsThisLevel = deepcopy(varDomains)
            boardThisLevel = deepcopy(board)
            updateBoard(boardThisLevel, var, domainItem, n)
            newDomain = forwardChecking(varDomainsThisLevel, boardThisLevel, n)
            for i in newDomain:
                dictForSort[domainItem]= dictForSort[domainItem]+i.getDomainLen()

    sort_orders = sorted(dictForSort.items(), key=lambda x: x[1], reverse=True)
    sortedArr = []
    for i in sort_orders:
        sortedArr.append(i[0])

    return domain


def updateBoard(board, name, v, n):
    res = [int(i) for i in bin(v)[2:]]
    while len(res) < n:
        res.insert(0, 0)
    if name[0] == 'R':
        rowNum = int(name[1:])
        for i in range(n):
            board[rowNum][i] = res[i]
        return

    if name[0] == 'C':
        colNum = int(name[1:])
        for i in range(n):
            board[i][colNum] = res[i]
        return


def printBoard(board, n):
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=" ")
        print()
    print(end="\n")


def backtrackingCSP(A, varDomains, n, board):
    if completenessChecker(A, n):
        return A

    X = MCV(A, varDomains)
    D = LCV(X.getName(), X.getDomain(),varDomains, board,n)

    for v in D:
        domain = deepcopy(varDomains)
        boardThisLevel = deepcopy(board)

        A[X.getName()] = v
        updateBoard(boardThisLevel, X.getName(), v, n)
        domain = forwardChecking(deepcopy(domain), boardThisLevel, n)

        if isThereEmptyVariable(domain):
            if v == D[-1]:
                return False
            else:
                A.pop(X.getName())
                continue

        result = backtrackingCSP(deepcopy(A), deepcopy(domain), n, boardThisLevel)

        if result:
            TablesList.append((deepcopy(boardThisLevel), X.getName()))
            # printBoard(board, n)
            return result
        A.pop(X.getName())

    return False
