# -*- coding: utf-8 -*-
# a = input("212121212324:")
# if a == 1:
#     b = 4

class mm:
    def __init__(self):
        self.a = 1
        self.b = 2

    # def __str__(self):
    #     return  str(self.a) + "." + str(self.b)


if __name__ == '__main__':

    everyDayGoodsList = [0] * 5
    chiocenessGoodsList = [1] * 5
    for goodsId in everyDayGoodsList + chiocenessGoodsList:
        print(goodsId)

    a = everyDayGoodsList and chiocenessGoodsList
    print(a)
    m1 = mm()
    m2 = mm()
    print(m1, m2)
