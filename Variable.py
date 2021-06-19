from copy import deepcopy


class Variable:

    def __init__(self, name):
        self.__name = name
        self.__domain = []
        self.__domainLen = 0

    def getName(self):
        return self.__name

    def getDomain(self):
        return self.__domain

    def setName(self, name):
        self.__name = name

    def getDomainLen(self):
        return self.__domainLen

    def addDomain(self, variable):
        self.__domain.append(deepcopy(variable))
        self.__domainLen = len(self.__domain)

    def setDomain(self, domain):
        self.__domain = deepcopy(domain)
        self.__domainLen = len(self.__domain)