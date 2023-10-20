# -*- coding: utf-8 -*-
# import abc


# class A(metaclass=abc.ABCMeta):
import functools


# class Cat:
#     """类注释，这是一只猫的类"""
#
#     # @abc.abstractmethod
#     def __init__(self, name, age):
#         self.name = name
#         self.__age = age  # 私有属性 (前面加_类名 就可以访问)
#         print("我是一只猫，我叫%s" % self.name)
#
#     def __del__(self):
#         # print("我被杰克辣条(徐志辉)虐待，消失在世界上了！")
#         pass
#
#     def __call__(self, *args, **kwargs):
#         """使类可以像函数一样被调用"""
#         print(args[0] + args[1])
#
#     def __str__(self):
#         return "我是%s" % self.name
#
#     def __len__(self):
#         return self.__age
#
#     def __iter__(self):
#         return iter([1, 23, 4, 5])
#
#     def __getitem__(self, key):
#         if key == "name":
#             return self.name
#         else:
#             return None
#
#     def __setitem__(self, key, val):
#         if key == "name":
#             self.name = val
#
#     def __delitem__(self, key):
#         if key == "name":
#             del self.name
#
#     def __add__(self, other):
#         if isinstance(other, Cat):
#             return [self, other]
#         elif isinstance(other, list):
#             other.append(self)
#             return other
#
#     def a(self):
#         pass
#
#
# if __name__ == '__main__':
#     cat = Cat("nainiu", 2)
#     # __doc__  __module__  __class__
#     print(cat.__doc__)  # 类注释，这是一只猫的类
#     print(cat.__module__)  # 类所在的模块名
#     print(cat.__class__)  # 对象所属类
#
#     # __call__
#     cat(1, 2)  # 调用cat
#     print("__call__:%s" % callable(cat))  # 检查对象是否可以被调用
#
#     # __dict__
#     print("__dict__:%s" % cat.__dict__)  # {'name': 'nainiu'}
#
#     # __str__
#     # 原输出<__main__.Cat object at 0x000001DF24C4D2E8> 加上__str__输出为我是nainiu
#     print("__str__:%s" % str(cat))
#     print("__str__:%s" % cat)
#
#     # __len__
#     print("__len__:%s" % len(cat))
#
#     # __iter__ 添加可迭代的魔法方法
#     # iterable iter #迭代
#     for i in cat:
#         print("__iter__:%s" % i)
#
#     # __getitem__ __setitem__  __delitem__
#     # {'name': 'nainiu', '_Cat__age': 2}
#     print("__getitem__:%s" % cat["name"])
#     cat["name"] = "piegg"
#     print("__setitem__修改后:%s" % cat["name"])
#     # del cat["name"]
#
#     # __add__:+   __sub__:-  __mul__:*  __div__:/  __mod__:%  __pow__:**
#     cat1 = Cat("nainiu1", 2)
#     cat2 = Cat("nainiu2", 2)
#
#     cats = cat1 + cat2
#     print("__add__:%s" % cats)
#     cat3 = Cat("nainiu3", 2)
#     print("__add__:%s" % (cat3 + cats))


@functools.lru_cache()
def add_user(a):
    return a + a
    # # user = UserInfo(name="李四")


if __name__ == '__main__':
    add_user(1)
    add_user(1)
    # print(dir(add_user))
    print(add_user.cache_info())
    print(add_user.cache_clear())
    print(type(add_user.cache_info()))
