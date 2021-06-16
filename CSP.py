import random
from copy import deepcopy
import numpy
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
    for row in range(len(board)):
        if not '-' in ''.join(map(str, board[row])):
            for i in varDomain:
                if int(''.join(map(str, board[row])), 2) in i.getDomain() and 'R' in i.getName():
                    if int(i.getName()[1:]) != row:
                        # print(i.getName(),"  -R-  ",i.getDomain())
                        # print(row)
                        i.getDomain().remove(int(''.join(map(str, board[row])), 2))

    boardR = numpy.array(board)
    boardR = boardR.T
    for column in range(len(boardR)):
        if not '-' in ''.join(map(str, boardR[column])):
            for i in varDomain:
                if int(''.join(map(str, boardR[column])), 2) in i.getDomain() and 'C' in i.getName():
                    if int(i.getName()[1:]) != column:
                        # print(i.getName(),"  -C-  ",i.getDomain())
                        # print(column)
                        i.getDomain().remove(int(''.join(map(str, boardR[column])), 2))

    makeRowNodeConsistent(n, board, varDomain)
    makeColNodeConsistent(n, board, varDomain)

    # print("_______________________________")

    return varDomain


def LCV(var, domain, board):
    # print(domain)
    # print(var, " : ", domain)
    printBoard(board, len(board))
    boardR = numpy.array(board).T
    printBoard(boardR, len(boardR))
    num = int(var[1:])
    dictForSort = {}

    if 'C' in var:
        for domainItem in domain:
            dictForSort[domainItem] = 0
            binaryDomainItem = [int(i) for i in bin(domainItem)[2:]]
            while len(binaryDomainItem) < len(board):
                binaryDomainItem.insert(0, 0)
            for boardItem in boardR:
                if not '-' in ''.join(map(str, boardItem)):
                    if int(''.join(map(str, boardItem)), 2) == domainItem:
                        dictForSort[domainItem] = dictForSort[domainItem] - 1


            for item in range(len(boardR[num])):
                if str(boardR[num][item]) != '-' :
                    if int(boardR[num][item]) != int(binaryDomainItem[item]):
                            dictForSort[domainItem] = dictForSort[domainItem] - 1



    elif 'R' in var:
        for domainItem in domain:
            dictForSort[domainItem] = 0
            binaryDomainItem = [int(i) for i in bin(domainItem)[2:]]
            while len(binaryDomainItem) < len(board):
                binaryDomainItem.insert(0, 0)
            for boardItem in board:
                if not '-' in ''.join(map(str, boardItem)):
                    if int(''.join(map(str, boardItem)), 2) == domainItem:
                        dictForSort[domainItem] = dictForSort[domainItem] - 1
        for item in range(len(board[num])):
            if str(board[num][item]) != '-':
                if int(board[num][item]) != int(binaryDomainItem[item]):
                    dictForSort[domainItem] = dictForSort[domainItem] - 1
    # for i in dictForSort.keys():
        # print(i," = ",dictForSort[i])

    sort_orders = sorted(dictForSort.items(), key=lambda x: x[1], reverse=True)
    sortedArr = []
    for i in sort_orders:
        sortedArr.append(i[0])
    # print(sortedArr)

    return sortedArr


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
    print(end="\n")


def backtrackingCSP(A, varDomains, n, board):
    if completenessChecker(A, n):
        return A

    X = MCV(A, varDomains)
    D = LCV(X.getName(), X.getDomain(), board)

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
            # printBoard(board, n)
            return result
        A.pop(X.getName())

    return False
