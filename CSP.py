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


def forwardChecking(varDomain):
    # vv = deepcopy(varDomain)
    # for i in varDomain:
    #     print("\n", i.getName(), "  :  ", i.getDomain(), end="-")
    checking(varDomain)
    # for i in varDomain:
    #     print("\n", i.getName(), "  :::  ", i.getDomain(), end="-")
    tempDict = {}
    for dName in varDomain:
        tempLst = []
        for d in dName.getDomain():
            res = [int(i) for i in bin(d)[2:]]
            while len(res) < len(varDomain) / 2:
                res.insert(0, 0)
            tempLst.append(res)
        tempDict[dName.getName()] = tempLst

    for i in tempDict.keys():
        print("\n",i," --:-- ",tempDict[i])

    for i in varDomain:
        print("\n",i.getName()," -:- ",i.getDomain())

    for row in range(len(varDomain) // 2):
        for column in range(len(varDomain) // 2):
            for rowDomainMember in tempDict["R" + str(row)]:
                for columnDomainMember in tempDict["C" + str(column)]:
                    print( "row:",row ,"  -  ", "column:", column)
                    if rowDomainMember[column] != columnDomainMember[row]:
                        print("yes!")
                        print("row:", rowDomainMember, "  -  ", "column:", columnDomainMember)

                        tempDict["C" + str(column)].remove(columnDomainMember)
                    else:
                        print("no!")
                        print("row:", rowDomainMember, "  -  ", "column:", columnDomainMember)
                    print()

    for i in tempDict.keys():
        # print("\n-", i, "-:- ")
        for k in varDomain:
            if i in k.getName():
                k.getDomain().clear()
                for j in tempDict[i]:
                    k.addDomain(binaryToDecimal(int("".join([str(int) for int in j]))))
    print("last var domains:")
    for i in varDomain:
        print(i.getName(), " : ", i.getDomain())

    print()

    return varDomain


def binaryToDecimal(binary):
    decimal, i, n = 0, 0, 0
    while (binary != 0):
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


def backtrackingCSP(A, varDomains, n):
    if completenessChecker(A, n):
        return A

    X = MCV(A, varDomains)
    D = LCV(X.getDomain())

    for v in D:
        # print(X.getName(), " !! ", v)
        A[X.getName()] = v

        varDomains = forwardChecking(varDomains)  # forwardChecking(varDomains, X, v, A)

        if isThereEmptyVariable(varDomains):
            return False

        result = backtrackingCSP(A, varDomains, n)

        if result:
            return result
        A[X] = None

    return False
