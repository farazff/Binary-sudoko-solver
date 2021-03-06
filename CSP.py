import binhex
import random
from copy import deepcopy

import numpy

TablesList = []


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


def getTablesList():
    return TablesList


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


def LCV(var, domain, varDomains, board, n):
    dictForSort = {}
    for domainItem in domain:
        dictForSort[domainItem] = 0
        varDomainsThisLevel = deepcopy(varDomains)
        boardThisLevel = deepcopy(board)
        updateBoard(boardThisLevel, var, domainItem, n)
        newDomain = forwardChecking(varDomainsThisLevel, boardThisLevel, n)
        for i in newDomain:
            dictForSort[domainItem] = dictForSort[domainItem] + i.getDomainLen()

    sort_orders = sorted(dictForSort.items(), key=lambda x: x[1], reverse=True)
    sortedArr = []
    for i in sort_orders:
        sortedArr.append(i[0])

    return sortedArr


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


def AC3(A, queue, varDomain, n):
    while len(queue) > 0:
        (xi, xj) = queue.pop(0)
        if revise(varDomain, xi, xj, n):
            if len(varDomain[xi].getDomain()) == 0:
                return False
            for var in varDomain:
                if var.getName() != varDomain[xi].getName():
                    if var.getName() != varDomain[xj].getName() and var.getName() not in A:
                        if var.getName()[0] == 'R':
                            num = int(var.getName()[1:])
                        else:
                            num = int(var.getName()[1:]) + n

                        queue.append((num, int(xi)))
    return varDomain


def revise(varsDomain, xi, xj, n):
    revised = False
    newDomain = []

    for varXI in varsDomain[xi].getDomain():
        found = False
        if str(varsDomain[xi].getName()[0]) == str(varsDomain[xj].getName()[0]):
            for JDomain in varsDomain[xj].getDomain():
                if JDomain != varXI:
                    found = True
                    break

        else:
            if str(varsDomain[xi].getName()[0]) == 'R' and str(varsDomain[xj].getName()[0]) == "C":
                xiRow = int(varsDomain[xi].getName()[1:])
                xjCol = int(varsDomain[xj].getName()[1:])
                resI = [int(i) for i in bin(varXI)[2:]]
                while len(resI) < n:
                    resI.insert(0, 0)

                toBeInJ = resI[xjCol]
                for varXJ in varsDomain[xj].getDomain():
                    resJ = [int(i) for i in bin(varXJ)[2:]]
                    while len(resJ) < n:
                        resJ.insert(0, 0)
                    if resJ[xiRow] == toBeInJ:
                        found = True
                        break

            if str(varsDomain[xi].getName()[0]) == 'C' and str(varsDomain[xj].getName()[0]) == "R":
                xiCol = int(varsDomain[xi].getName()[1:])
                xjRow = int(varsDomain[xj].getName()[1:])
                resI = [int(i) for i in bin(varXI)[2:]]
                while len(resI) < n:
                    resI.insert(0, 0)

                toBeInJ = resI[xjRow]
                for varXJ in varsDomain[xj].getDomain():
                    resJ = [int(i) for i in bin(varXJ)[2:]]
                    while len(resJ) < n:
                        resJ.insert(0, 0)
                    if resJ[xiCol] == toBeInJ:
                        found = True
                        break

        if found is False:
            revised = True
        else:
            newDomain.append(deepcopy(varXI))

    varsDomain[xi].setDomain(deepcopy(newDomain))
    return revised


def MAC(A, varDomains, X, domain, n, v):
    listToAC3 = []
    for var in varDomains:
        if var.getName() in A or var.getName() == X.getName():
            pass
        else:
            if var.getName()[0] == 'R':
                num1 = int(var.getName()[1:])
            else:
                num1 = int(var.getName()[1:]) + n

            if X.getName()[0] == 'R':
                num2 = int(X.getName()[1:])
            else:
                num2 = int(X.getName()[1:]) + n
            listToAC3.append((num1, num2))

    for i in domain:
        if i.getName() == X.getName():
            i.setDomain([v])
            break

    domain = AC3(A, listToAC3, deepcopy(domain), n)
    return domain


def backtrackingCSP(A, varDomains, n, board, doForward):
    if completenessChecker(A, n):
        return A

    X = MCV(A, varDomains)
    D = LCV(X.getName(), X.getDomain(), varDomains, board, n)

    for v in D:
        domain = deepcopy(varDomains)
        boardThisLevel = deepcopy(board)
        A[X.getName()] = v
        updateBoard(boardThisLevel, X.getName(), v, n)

        if doForward is True:
            domain = forwardChecking(deepcopy(domain), boardThisLevel, n)
        else:
            domain = MAC(A, varDomains, X, domain, n, v)

        if domain is False or isThereEmptyVariable(domain):
            if v == D[-1]:
                return False
            else:
                A.pop(X.getName())
                continue

        result = backtrackingCSP(deepcopy(A), deepcopy(domain), n, boardThisLevel, doForward)

        if result:
            TablesList.append((deepcopy(boardThisLevel), X.getName()))
            return result
        A.pop(X.getName())

    return False