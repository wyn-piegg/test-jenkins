# # -*- coding: utf-8 -*-
# oneGoods = []
# towGoods = []
# threeGoods = []
# fourGoods = []
# fiveGoods = []
# sixGoods = []
# for goodsId, goodsIfo in _goods_info.items():
#     if goodsIfo.price == 0:
#         oneGoods.append(goodsId)
#     if goodsIfo.quality == 1 or goodsIfo.quality == 2:
#         towGoods.append(goodsId)
#     if goodsIfo.quality == 3 or goodsIfo.quality == 4:
#         threeGoods.append(goodsId)
# dayGoodsIdDict = {1: oneGoods, 2: towGoods, 3: threeGoods}
# for goodsId, goodsIfo in _goods_info.items():
#     if goodsIfo.shopId == 2:
#         if goodsIfo.quality == 1:
#             oneGoods.append(goodsId)
#         if goodsIfo.quality == 2:
#             towGoods.append(goodsId)
#         if goodsIfo.quality == 3:
#             threeGoods.append(goodsId)
#         if goodsIfo.quality == 4:
#             fourGoods.append(goodsId)
#         if goodsIfo.quality == 5:
#             fiveGoods.append(goodsId)
#         if goodsIfo.quality == 6:
#             sixGoods.append(goodsId)
# chioceGoodsIdDict = {1: oneGoods, 2: towGoods, 3: threeGoods, 4: fourGoods, 5: fiveGoods, 6: sixGoods}
# # 每日商城刷新
# dayGoodsList = [random.choice(dayGoodsIdDict.get(1)), random.sample(dayGoodsIdDict.get(2), 5),
#                 random.sample(dayGoodsIdDict.get(3), 2)]
# # 精选商城刷新
# chiocenessGoods = []
# for quality, goods in chioceGoodsIdDict.items():
#     chiocenessGoods.append(random.choice(goods))
# print(chiocenessGoods)
# return dayGoodsList, chiocenessGoods
