# -*- coding: utf-8 -*-
# a = [1, 2, 3, 4, 5, 6, 7, 8]
# b = {111:{111:{'a':1}}}
# for k,v in b.items():
#     idList = list(v.values())[0]
# scoresList = []
# for i in range(0, len(a)):
#     if i % 2 == 0:
#         idList.append(a[i])
# print(idList)
a = {1: "ti", 2: "ct"}
c = {"ti": 23}
print(c.get(a.get(1)))
