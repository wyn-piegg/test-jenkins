# -*- coding: utf-8 -*-
import random
info = []
a = [1, 2, 3, 6, 5, 4, 9, 8, 7, 45, 16, 897, 654, 136, 95]
b = [5, 69, 85, 99, 456, 888, 45, 12, 2, 1, 10, 65, 98, 67, 145]
d = a.copy()
c = b.copy()
for i in range(0, 6):
    df = random.choices(d, c, k=1)
    for dd in df:
        idx = d.index(dd)
        d.remove(dd)
        c.remove(c[idx])
        info.append(dd)
print(info)
ddd = []
dict1 = {1: [2, 65, 88, 54, 66, 8888, 555, 55, 15, 224, 48], 2: [1, 3, 6, 5, 4, 9, 8, 7, 45, 16, 897, 654, 136, 95]}
dict2 = {1: [2, 65, 88, 54, 66, 8888, 555, 55, 15, 224, 48], 2: [1, 3, 6, 5, 4, 9, 8, 7, 45, 16, 897, 654, 136, 95]}
info = []
for i in range(0, 10):
    info.append(random.sample(dict1.get(1), 1))
print(info)
for i in info:
    print(i)

for i in range(0, 6):
    df = random.choices(dict1.get(2), dict2.get(2), k=1)
    for dd in df:
        idx = dict1.get(2).index(dd)
        dict1.get(2).remove(dd)
        dict2.get(2).remove(dict2.get(2)[idx])
        ddd.append(dd)
print(ddd)
now = list(set(info))
if len(now) != 0:
    pass
print(now)
print(info)
info.extend(random.choices(a, b, k=len(list(set(info)))))
print(info)

a=None
a=1

