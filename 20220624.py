# import random, time
#
# # 时间戳
# now_time = time.time()
# # 毫秒级时间戳
# point = round(now_time * 10000)
# # 写入随机数，同一时间，随机种子
# random.seed(point)
# #生成条数
# count = 10
# #生成随机数的随机长度10-15
# length = random.randint(10, 15)
# #随机生成字符串
# def create_num():
#     #将字符串123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ中的每个成员以空格分隔开再拼接成一个字符串
#     random_num_str = ''.join(random.sample('123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ', length)).replace("", "")
#     return random_num_str
#
# result = {1: create_num()}
# def check():
#     #新产生的字符串
#     new_create_num = create_num()
#     #字符串不重复
#     for new_check in result:
#         if result[new_check] != new_create_num:
#             return new_create_num
#         else:
#             check()
# for num in range(2, count + 1):
#     result[num] = check()
# #输出第几条激活码是什么
# for repeat_check in result:
#     print('第%s条激活码:' % (repeat_check),result[repeat_check])

#
# import time
#
# # 注 机器ID占位5 这也就意味者十进制下编号不能超过31  将机器ID与机房ID合并，最大三个机房即00 10 20 每个机房的数值 + 1 即是机器ID  备用 30 31
# WORKER_ID_BITS = 5
# SEQUENCE_BITS = 12
#
# # 最大取值计算
# MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
#
# # 移位偏移计算
# WORKER_ID_SHIFT = SEQUENCE_BITS
# TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
# # print(WORKER_ID_SHIFT, TIMESTAMP_LEFT_SHIFT)
#
# # 序号循环掩码
# SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)
# # print(SEQUENCE_MASK)
#
# # 起始时间
# TWEPOCH = 1594977661913
#
#
# class IdWorker(object):
#
#     def __init__(self, worker_id, sequence=0):
#         """
#         :param worker_id: 机房和机器的ID 最大编号可为00 - 31  实际使用范围 00 - 29  备用 30 31
#         :param sequence: 初始码56432
#         """
#         if worker_id > MAX_WORKER_ID or worker_id < 0:
#             raise ValueError('worker_id值越界')
#
#         self.worker_id = worker_id
#         self.sequence = sequence
#         self.last_timestamp = -1  # 上次计算的时间戳
#
#     def get_timestamp(self):
#         """
#         生成毫秒级时间戳
#         :return: 毫秒级时间戳
#         """
#         return int(time.time() * 1000)
#
#     def wait_next_millis(self, last_timestamp):
#         """
#         等到下一毫秒
#         """
#         timestamp = self.get_timestamp()
#         while timestamp <= last_timestamp:
#             timestamp = self.get_timestamp()
#         return timestamp
#
#     def get_id(self):
#         """"""
#         timestamp = self.get_timestamp()
#         # 判断服务器的时间是否发生了错乱或者回拨
#         if timestamp < self.last_timestamp:
#             # 如果服务器发生错乱 应该抛出异常
#             # 此处待完善
#             pass
#
#         if timestamp == self.last_timestamp:
#             self.sequence = (self.sequence + 1) & SEQUENCE_MASK
#             if self.sequence == 0:
#                 timestamp = self.wait_next_millis(self.last_timestamp)
#         else:
#             self.sequence = 0
#         self.last_timestamp = timestamp
#         new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.worker_id << WORKER_ID_SHIFT) | self.sequence
#         return new_id
#
#
# if __name__ == '__main__':
#     # 测试效率
#     import datetime
#
#     worker = IdWorker(worker_id=1, sequence=0)
#     ids = []
#     start = datetime.datetime.now()
#     for i in range(1000000):
#         new_id = worker.get_id()
#         ids.append(new_id)
#     end = datetime.datetime.now()
#     spend_time = end - start
#     print(spend_time, len(ids), len(set(ids)))
import random, time

# 获取时间戳
now_time = time.time()
# 毫秒级时间戳
point = round(now_time * 10000)
# 写入随机数
random.seed(point)

count = 10
box = []
# 快速生成字母
small = [chr(i) for i in range(97, 123)]
big = [chr(i) for i in range(65, 91)]
number = [str(i) for i in range(1, 10)]

for i in range(count):
    data_str = ""
    # 生成随机字符串（长度18）
    for j in range(4):
        # 字符串拼接
        data = random.choice(small) + random.choice(big) + random.choice(number)
        data_str += data
        # print(data)
    # 再次打乱
    data_list = list(data_str)
    # shuffle()方法将序列的所有元素随机排序。
    random.shuffle(data_list)
    # 将data_list列表里的元素重新拼接为字符串
    data_str = "".join(data_str)
    # 随机截取10到15的长度
    random_count = random.choices(data_str,k=10)
    # 第三次打乱
    result_list = list(random_count)
    # shuffle()方法将序列的所有元素随机排序。
    random.shuffle(result_list)
    result = "".join(result_list)
    print(result)
    # 替换O,o,0
    result = result.replace("O", random.choice(big))
    result = result.replace("o", random.choice(small))
    result = result.replace("0", random.choice(number))
    print("激活码:", result, "长度:", len(result))
    box.append(result)
print(box)

























