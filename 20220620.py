#
#
#
#
# # age = int(input("请输入你家狗狗的年龄: "))
# # print("")
# # if age <= 0:
# #     print("你是在逗我吧!")
# # elif age == 1:
# #     print("相当于 14 岁的人。")
# # elif age == 2:
# #     print("相当于 22 岁的人。")
# # elif age > 2:
# #     human = 22 + (age - 2) * 5
# #     print("对应人类年龄: ", human)
# # ### 退出提示
# # input("点击 enter 键退出")
#
# print('--------------------------------------------------------------------------------- ')
#
#
# var1 = 100
# if var1:
#     print("1 - if 表达式条件为 true")
#     print(var1)
#
# var2 = 0
# if var2:
#     print("2 - if 表达式条件为 true")
#     print(var2)
# print("Good bye!")
# print('--------------------------------------------------------------------------------- ')
#
print('{}网址： {}!'.format('菜鸟教程', 'www.runoob.com'))

import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456'
                     )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
db.close()


class Mx:
    def __init__(self, name, age):
        self.name = name
        self.age = age
d = Mx('羡羡',3)
print('{0}今年{1}岁了。'.format(d.name,d.age))


print("----------------------------->>")


# 类定义
class people:
    # 定义基本属性
    name = ''
    age = 0
    # 定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0
    # 定义构造方法
    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %s 岁。" % (self.name, self.age))


# 单继承示例
class student(people):
    grade = ''
    def __init__(self, n, a, w, g):
        # 调用父类的构函
        people.__init__(self, n, a, w)
        self.grade = g
    # 覆写父类的方法
    def speak(self):
        print("%s 说: 我 %s 岁了，我在读 %s 年级" % (self.name, self.age, self.grade))
s = student('ken', 10, 60, 3)
s.speak()