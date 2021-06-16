# class State:
#     def __init__(self, n):
#         self.__table = [[] for i in range(n)]
#
#     @property
#     def table(self):
#         return self.__table
#
#     @table.setter
#     def table(self, newTable):
#         self.__table = newTable
orders = {
	'cappuccino': 54,
	'latte': 56,
	'espresso': 72,
	'americano': 48,
	'cortado': 41
}

sort_orders = sorted(orders.items(), key=lambda x: x[1], reverse=True)
sortedArr=[]
for i in sort_orders:
    sortedArr.append(i[0])
print(sorted)