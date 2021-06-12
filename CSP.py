import random
from copy import deepcopy


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
    print(A)
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


def forwardChecking(varDomain):
    # TODO: Complete this function
    return varDomain


def LCV(domain):
    # TODO: Complete LCV
    return domain


def backtrackingCSP(A, varDomains, n):
    if completenessChecker(A, n):
        return A

    X = MCV(A, varDomains)
    D = LCV(X.getDomain())

    for v in D:
        print(X.getName(), " !! ", v)
        A[X.getName()] = v

        varDomains = forwardChecking(varDomains)  # forwardChecking(varDomains, X, v, A)

        if isThereEmptyVariable(varDomains):
            return False

        result = backtrackingCSP(A, varDomains, n)

        if result:
            return result
        A[X] = None

    return False
