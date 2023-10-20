# -*- coding: utf-8 -*-
import random
from dataclasses import dataclass

import d_shopping

_goods_info = {}
_goods_shop = {}
_goods_script = {1: "LimitGoods", 2: "LimitGoods", 3: "GoodsConfig", 4: "MultipleGoods"}
_shop_script = {1: "DayShop", 2: "ChoiceShop", 3: "Shop", 4: "Shop"}


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

        _goods_shop.setdefault(shopId, eval(_shop_script[shopId])()).addGoods(scriptInst)


class Shop:
    def __init__(self):
        self.goodsIdDict = {}
        self.randomDict = {}

    def addGoods(self, goodsInfo):
        self.goodsIdDict.setdefault(goodsInfo.goodsId, goodsInfo)


class DayShop(Shop):
    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(DayShop, self).addGoods(goodsInfo)
        if goodsInfo.price == 0:
            self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)
        if goodsInfo.quality == 1 or goodsInfo.quality == 2:
            self.randomDict.setdefault(2, []).append(goodsInfo.goodsId)
        if goodsInfo.quality == 3 or goodsInfo.quality == 4:
            self.randomDict.setdefault(3, []).append(goodsInfo.goodsId)

    def getRandomGoods(self):
        dayGoodsList = [random.choice(self.randomDict.get(1)), random.sample(self.randomDict.get(2), 5),
                        random.sample(self.randomDict.get(3), 2)]
        return dayGoodsList


class ChoiceShop(Shop):
    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(ChoiceShop, self).addGoods(goodsInfo)
        self.goodsIdDict.setdefault(goodsInfo.priceQuality, []).append(goodsInfo.goodsId)
        return self.goodsIdDict

    def getRandomGoods(self):
        return [random.choice(goods) for goods in self.randomDict.values()]


if __name__ == '__main__':
    onInit()
