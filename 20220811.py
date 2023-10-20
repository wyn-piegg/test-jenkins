# -*- coding: utf-8 -*-
talent = {1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 3, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0]}
ntalentCountList = []
for k, v in talent.items():
    ntalentCountList.append(v)
print(ntalentCountList)

ntalentCountList[1][2] += 1
print(ntalentCountList[1][2])


def savePoint(talent):
    ntalentCountList = []
    for k, v in talent:
        ntalentCountList.append(v)
    print(ntalentCountList)
    print(ntalentCountList[1][2])




p=[1,2,3]
print(sum(p))
