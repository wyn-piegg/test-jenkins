# # -*- coding=utf-8 -*-
# # author: Pegasus
# # time: 2021/04/01 11:25
# # 生成由大写英文字母和数字组成的激活码
#
# import random
# import string
#
# number = 30  # 激活码的数量
# length = 12  # 激活码的长度
#
#
# def made():  # 生成激活码
#     # activation_code = string.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456',length)).replace(" ","")#python2语法
#     activation_code = ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length)).replace(" ",
#                                                                                                      "")  # python3语法
#     return activation_code
#
#
# a = {1: made()}
#
#
# # print('生成数量：',a)
# def judge():  # 判断生成的激活码是否和字典中存在的激活码重复
#     new_made = made()
#     for k in a:
#         if a[k] != new_made:
#             return new_made
#         else:
#             judge()
#
#
# for i in range(2, number + 1):
#     a[i] = judge()
#
# for j in a:
#     print('%4d' % (j), '   ', a[j])




import random, time
# 时间戳
now_time = time.time()
# 毫秒级时间戳
point = round(now_time * 10000)
# 写入随机数
random.seed(point)
count = 10
length = random.randint(10, 15)
def create_num():
    random_num_str = ''.join(random.sample('123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ', length)).replace(" ", "")
    return random_num_str
result = {1: create_num()}
def check():
    new_create_num = create_num()
    for new_check in result:
        if result[new_check] != new_create_num:
            return new_create_num
        else:
            check()
for num in range(2, count + 1):
    result[num] = check()
for repeat_check in result:
    print('%4d' % (repeat_check), '', result[repeat_check])