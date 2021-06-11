from copy import deepcopy


class Variable:

    def __init__(self, name):
        self.__name = name
        self.__domain = []

    def getName(self):
        return self.__name

    def getDomain(self):
        return self.__domain

    def setName(self, name):
        self.__name = name

    def addDomain(self, variable):
        self.__domain.append(deepcopy(variable))

    def setDomain(self, domain):
        self.__domain = deepcopy(domain)
