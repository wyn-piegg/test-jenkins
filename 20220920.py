# -*- coding: utf-8 -*-
import random
from dataclasses import dataclass

import d_shopping

_goods_info = {}

_goods_script = {1: "LimitGoods", 2: "LimitGoods", 3: "GoodsConfig", 4: "MultipleGoods"}
_goods_shop = {1: "dayGoods", 2: "chiocenessGoods", 3: "shop", 4: "currencyGoods"}


@dataclass
class GoodsConfig:
    # 商品id
    goodsId: int = 0
    # 商店id
    shopId: int = 0
    # 道具id
    itemId: int = 0
    # 道具数量
    itemCount: int = 0
    # 价格
    price: int = 0
    # 货币类型
    priceType: int = 0
    # 道具品质
    quality: int = 0
    # 价格档位
    priceQuality: int = 0
    # 商品状态
    goodsState: int = 0
    # 商品可购买几次
    buyCount: int = 0

    def checkLimit(self, goodsBuyInfo):
        if self.buyCount != 0 and goodsBuyInfo.getData(self.goodsId) >= self.buyCount:
            return False

    def giveItem(self, goodsBuyInfo):
        return self.itemCount

    def setGoodsBuyCount(self, goodsBuyInfo):
        goodsBuyInfo.addData(1)


class LimitGoods(GoodsConfig):
    def giveItem(self, goodsBuyInfo):
        return self.itemCount


class MultipleGoods(GoodsConfig):
    def giveItem(self, goodsBuyInfo):
        buyCount = goodsBuyInfo.getData(self.goodsId)
        return self.itemCount * 2 if buyCount == 0 else self.itemCount



def onInit():
    Goods = GoodsConfig()
    for goodsId, goodsInfo in d_shopping.datas.items():
        Goods.goodsId = goodsId
        shopId = goodsInfo.get('shopId')
        itemId = goodsInfo.get('itemId')
        itemCount = goodsInfo.get('itemCount')
        price = goodsInfo.get('price')
        priceType = goodsInfo.get('priceType')
        quality = goodsInfo.get('quality')
        priceQuality = goodsInfo.get('priceQuality')
        goodsState = goodsInfo.get('goodsState')
        buyCount = goodsInfo.get('buyCount')

        script = _goods_script.get(shopId)
        scriptInst = eval(script)(goodsId=goodsId,
                                  shopId=shopId,
                                  itemId=itemId,
                                  itemCount=itemCount,
                                  price=price,
                                  priceType=priceType,
                                  quality=quality,
                                  priceQuality=priceQuality,
                                  goodsState=goodsState,
                                  buyCount=buyCount)

        _goods_info[goodsId] = scriptInst

        _goods_shop.setdefault(shopId, shop()).addGoods(scriptInst)


class shop:
    def __init__(self):
        self.dayGoodsIdDict = {}
        self.chioceGoodsIdDict = {}
        self.currencyGoodsOneDict = {}
        self.currencyGoodsTwoDict = {}
        self.currencyGoods = {3: self.currencyGoodsOneDict, 1: self.currencyGoodsTwoDict}

    # def addGoods(self, goodsInfo):
    #     if goodsInfo.price == 0:
    #         self.dayGoodsIdDict.setdefault(1, []).append(goodsInfo.goodsId)
    #     if goodsInfo.quality == 1 or goodsInfo.quality == 2:
    #         self.dayGoodsIdDict.setdefault(2, []).append(goodsInfo.goodsId)
    #     if goodsInfo.quality == 3 or goodsInfo.quality == 4:
    #         self.dayGoodsIdDict.setdefault(3, []).append(goodsInfo.goodsId)

    def addGoods(self, goodsInfo):
        return goodsInfo.goodsId


class dayGoods(shop):
    def addGoods(self, goodsInfo):
        if goodsInfo.price == 0:
            self.dayGoodsIdDict.setdefault(1, []).append(goodsInfo.goodsId)
        if goodsInfo.quality == 1 or goodsInfo.quality == 2:
            self.dayGoodsIdDict.setdefault(2, []).append(goodsInfo.goodsId)
        if goodsInfo.quality == 3 or goodsInfo.quality == 4:
            self.dayGoodsIdDict.setdefault(3, []).append(goodsInfo.goodsId)
        return self.dayGoodsIdDict


class chiocenessGoods(shop):
    def addGoods(self, goodsInfo):
        self.chioceGoodsIdDict.setdefault(goodsInfo.priceQuality, []).append(goodsInfo.goodsId)
        return self.chioceGoodsIdDict


class currencyGoods(shop):
    def addGoods(self, goodsInfo):
        goods = self.currencyGoods.get(goodsInfo.priceType, None)
        if goods is None:
            return
        goods.setdefault(goodsInfo.priceQuality, []).append(goodsInfo.goodsId)
        return self.currencyGoods
    # def findGoods(self,):
    #     dayGoodsIdDict = {}
    #     for goodsId, goodsInfo in _goods_info.items():
    #         if goodsInfo.shopId == 1:
    #             if goodsInfo.price == 0:
    #                 dayGoodsIdDict.setdefault(1, []).append(goodsId)
    #             if goodsInfo.quality == 1 or goodsInfo.quality == 2:
    #                 dayGoodsIdDict.setdefault(2, []).append(goodsId)
    #             if goodsInfo.quality == 3 or goodsInfo.quality == 4:
    #                 dayGoodsIdDict.setdefault(3, []).append(goodsId)
    #
    #     chioceGoodsIdDict = {}
    #     for goodsId, goodsInfo in _goods_info.items():
    #         if goodsInfo.shopId == 2:
    #             chioceGoodsIdDict.setdefault(goodsInfo.priceQuality, []).append(goodsId)
    #
    #     currencyGoodsOneDict = {}
    #     for goodsId, goodsInfo in _goods_info.items():
    #         if goodsInfo.shopId == 4 and goodsInfo.priceType == 3:
    #             currencyGoodsOneDict.setdefault(goodsInfo.priceQuality, []).append(goodsId)
    #
    #     currencyGoodsTwoDict = {}
    #     for goodsId, goodsInfo in _goods_info.items():
    #         if goodsInfo.shopId == 4 and goodsInfo.priceType == 1:
    #             currencyGoodsTwoDict.setdefault(goodsInfo.priceQuality, []).append(goodsId)
    #
    #     _goods_shop[1] = dayGoodsIdDict
    #     _goods_shop[2] = chioceGoodsIdDict
    #     _goods_shop[""] = currencyGoodsOneDict
    #     _goods_shop[4 - 2] = currencyGoodsTwoDict


def getDayGoods():
    """
    刷新每日商城
    @return:
    """
    dayGoodsIdDict = _goods_shop.get(1)
    dayGoodsList = [random.choice(dayGoodsIdDict.get(1)), random.sample(dayGoodsIdDict.get(2), 5),
                    random.sample(dayGoodsIdDict.get(3), 2)]
    return dayGoodsList


def getChiocenessGoods():
    """
    刷新精选商城
    @return:
    """
    chioceGoodsIdDict = _goods_shop.get(2)
    return [random.choice(goods) for goods in chioceGoodsIdDict.values()]


def currencyShop():
    """
    货币商城
    @return:
    """
    currencyGoods = []

    for goods in currencyGoodsOneDict.values():
        currencyGoods.append(random.choice(goods))
    for goods in currencyGoodsTwoDict.values():
        currencyGoods.append(random.choice(goods))
    return currencyGoods


if __name__ == '__main__':
    onInit()
    shop = shop()
    shop.findGoods()

    # getChiocenessGoods()
    # currencyShop()
