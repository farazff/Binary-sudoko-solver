class State:
    def __init__(self, n):
        self.__table = [[] for i in range(n)]

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, newTable):
        self.__table = newTable