
def completenessChecker(َA):
    for i in َA.keys():
        if َA[i] == None:
            return False
    return True



def isThereEmptyVariable(varDomains):
    for i in varDomains.keys():
        if varDomains[i] == None:
            return False
    return True



def backtrackingCSP(A, varDomains):
    if completenessChecker(A):
        return A
    X = None  # MCV(A)
    D = None  # LCV(X)

    for v in D:
        A[X] = v

        varDomains = None  # forwardChecking(varDomains, X, v, A)

        if isThereEmptyVariable(A, varDomains):
            return False

        result = backtrackingCSP(A, varDomains)

        if result != False:
            return result
        A[X] = None

    return False
