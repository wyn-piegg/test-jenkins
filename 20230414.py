import random


def prepare_weighted_random4(values, weights):
    count = len(weights) - 1
    sum_ = 0

    # 计算总和
    for w in weights:
        sum_ = sum_ + w

    # 平均权重
    avg = sum_ / (count + 1)
    # 预生成
    aliases = {}
    for i in range(len(weights)):
        aliases.setdefault(i, [1, False])

    # 找到第1个小于平均值的索引
    sidx = 0
    while sidx <= count and weights[sidx] >= avg:
        sidx = sidx + 1

    # 如果 small_i > count 表示所有权重值相等，什么也不用处理
    if sidx <= count:
        small = [sidx, weights[sidx] / avg]

        # 找到第1个大于等于平均值的索引
        bidx = 0
        while bidx <= count and weights[bidx] < avg:
            bidx = bidx + 1
        big = [bidx, weights[bidx] / avg]

        while True:
            aliases[small[0]] = [small[1], big[0]]  # 桶的索引即是小权重的索引，从中去掉小权重的比例，剩余的放大权重
            big = [big[0], big[1] - (1 - small[1])]  # 大权重去掉已放入的比例
            if big[1] < 1:  # 如果大权重剩余的比例已小于1，表示小于平均权重
                small = big  # 大权重变成小权重

                bidx = bidx + 1  # 找下一个大权重的索引
                while bidx <= count and weights[bidx] < avg:
                    bidx = bidx + 1

                if bidx > count:
                    break
                big = [bidx, weights[bidx] / avg]  # 得到下一个大权重
            else:  # 大权重的比例大于等于1，表示不比平均权重小，继续找小权重
                sidx = sidx + 1
                while sidx <= count and weights[sidx] >= avg:
                    sidx = sidx + 1
                if sidx > count:
                    break
                small = [sidx, weights[sidx] / avg]

    def ret():
        n = random.random() * count
        i = int(n)
        odds, alias = aliases[i][0], aliases[i][1]
        if n - i > odds:
            idx = alias
        else:
            idx = i
        return values[idx], weights[idx]

    return ret()

# 运行
if __name__ == '__main__':
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    weights = [841, 395, 784, 799, 912, 198, 336, 769, 278, 554]
    prepare_weighted_random4(values, weights)