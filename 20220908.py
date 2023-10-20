# -*- coding: utf-8 -*-
from dataclasses import dataclass

foo = [[19, "zs"], [54, "ll"], [23, "wa"], [23, "df"], [23, "xf"]]
#
#
# a = sorted(foo, key=lambda x: (x[1], x[0]))
#
b = sorted(foo, key=lambda x: x[0])
#
# # 结果
# # >> > a
# # [['zs', 19], ['df', 23], ['wa', 23], ['xf', 23], ['ll', 54]]
# # >> > b
# # [['df', 23], ['ll', 54], ['wa', 23], ['xf', 23], ['zs', 19]]
# # >> >
# a = [[2, 3], [2, 1], [5, 6], [4, 3], [5, 3], [3, 3]]
# a.sort(key=lambda x: (x.sort(), x[0], x[1]))
print(b)

for i in range(0, 3):
    print(i)


class Text:
    def __init__(self, tttt, mmm):
        self.tttt = tttt
        self.__post_init__()

    def __str__(self):
       return "tttt=" + self.tttt


@dataclass
class Test:
    aa: int = 0
    bb: int = 0

    def __post_init__(self):
        self.aa = 11


if __name__ == '__main__':
    test = Text('llll', 0)
    print(test)
    test1 = Test(1)
    print(test1)
    test2 = Test(bb=9, aa=8)

    print(test2)
