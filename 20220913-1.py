# # -*- coding: utf-8 -*-
# import datetime
# import random
#
# import shop
# from KBEDebug import *
# from SHOP_INFO import ShopInfo
# from interfaces import CoinModule, BagModule
#
#
# class ShopModule:
#     def __init__(self):
#         self.everyDayRefreshNum = 5
#         self.chiocenessRefreshNum = 5
#         self.lastRefreshTime = 0
#         self.everyDayGoodsList = []
#         self.chiocenessGoodsList = []
#         self.seasonNum = 0
#
#     def shopping(self, goodId, goodsIdx, goodsId):
#         """
#         购买商品
#         @param goodsId:
#         @param goodId:
#         @param goodsIdx:
#         @return:
#         """
#         shop_result = []
#         if goodId == 1:
#             goodsList = self.everyDayGoodsList
#             if goodsList[goodsIdx] == 0:
#                 return
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(goodsId)
#             if CoinModule.checkCoinByType(self, priceType, price) is False:
#                 return
#             CoinModule.cutCoinHandle(self, priceType, price)
#             BagModule.addItemHandle(self, itemId, itemCount)
#             itemInfo = self.bagData.get(itemId, None)
#             current = itemInfo.getData('count')
#             shop_result.append(ShopInfo().createFromDict(
#                 {'itemId': itemId, 'count': current, 'price': price, 'priceType': priceType, 'quality': quality}))
#             goodsList[goodsIdx] = 0
#         if goodId == 2:
#             goodsList = self.chiocenessGoodsList
#             if goodsList[goodsIdx] == 0:
#                 return
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(goodsId)
#         if goodId == 4:
#             goodsList = shop.currencyShop()
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(goodsId)
#             for goodsIdx in range(0, 3):
#                 if goodsList[goodsIdx] == 0:
#                     BagModule.addItemHandle(self, itemId, itemCount)
#                 if goodsList[goodsIdx] == 1:
#                     BagModule.addItemHandle(self, itemId, itemCount * 2)
#             if priceType == 1:
#                 if CoinModule.checkCoinByType(self, priceType, price) is False:
#                     return
#                 CoinModule.cutCoinHandle(self, priceType, price)
#                 BagModule.addItemHandle(self, itemId, itemCount)
#                 itemInfo = self.bagData.get(itemId, None)
#                 current = itemInfo.getData('count')
#                 shop_result.append(ShopInfo().createFromDict(
#                     {'itemId': itemId, 'count': current, 'price': price, 'priceType': priceType, 'quality': quality}))
#
#         self.client.onShopping(shop_result)
#
#     def refresheveryDay(self):
#         """
#         刷新每日商城
#         @return:
#         """
#         everyDayGoodsResult = []
#         if self.everyDayRefreshNum <= 0:
#             return
#         everyDayGoods = shop.getEveryDayGoods()
#         self.everyDayRefreshNum -= 1
#         self.everyDayGoodsList = everyDayGoods
#         for i in self.everyDayGoodsList:
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(i)
#             everyDayGoodsResult.append(ShopInfo().createFromDict(
#                 {'itemId': itemId, 'count': itemCount, 'price': price, 'priceType': priceType, 'quality': quality}))
#         self.client.onRefreshDayShop(everyDayGoodsResult)
#
#     def refreshChioceness(self):
#         """
#         刷新精选商城
#         @return:
#         """
#         if self.chiocenessRefreshNum <= 0:
#             return
#         goodsIdDict = shop.getGoods(2)
#         ChiocenessGoodsResult = []
#         chiocenessGoods = []
#         for quality, goods in goodsIdDict.items():
#             chiocenessGoods.append(random.choice(goods))
#         self.chiocenessRefreshNum -= 1
#         self.chiocenessGoodsList = chiocenessGoods
#         for i in self.chiocenessGoodsList:
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(i)
#             ChiocenessGoodsResult.append(ShopInfo().createFromDict(
#                 {'itemId': itemId, 'count': itemCount, 'price': price, 'priceType': priceType, 'quality': quality}))
#         self.client.onRefreshChioceShop(ChiocenessGoodsResult)
#
#     def refreshShop(self):
#         """
#         定时刷新商店
#         @return:
#         """
#         everyDayGoodsResult = []
#         chiocenessGoodsResult = []
#         now_time = int(datetime.datetime.now().strftime("%Y%m%d"))
#         if now_time == self.lastRefreshTime:
#             return
#         self.everyDayGoodsList = shop.getEveryDayGoods()
#         self.chiocenessGoodsList = shop.getChiocenessGoods()
#         self.everyDayRefreshNum = 5
#         self.chiocenessRefreshNum = 5
#         self.lastRefreshTime = now_time
#         for i in self.everyDayGoodsList:
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(i)
#             everyDayGoodsResult.append(ShopInfo().createFromDict(
#                 {'itemId': itemId, 'count': itemCount, 'price': price, 'priceType': priceType, 'quality': quality}))
#         for i in self.chiocenessGoodsList:
#             itemId, itemCount, price, priceType, quality = shop.findGoodsInfo(i)
#             chiocenessGoodsResult.append(ShopInfo().createFromDict(
#                 {'itemId': itemId, 'count': itemCount, 'price': price, 'priceType': priceType, 'quality': quality}))
#         self.client.onRefreshShop(everyDayGoodsResult, chiocenessGoodsResult)
#
#     def refreshSeasonNum(self):
#         """
#         刷新赛季
#         @return:
#         """
