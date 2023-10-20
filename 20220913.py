# -*- coding: utf-8 -*-
import random

import d_shopping


def getGoods(shopId):
    """
    每日、精选商城的各个品质的商品
    @param shopId:
    @return:
    """
    oneGoods = []
    towGoods = []
    threeGoods = []
    fourGoods = []
    fiveGoods = []
    sixGoods = []
    goodsIdDict = {}
    if shopId == 1:
        for goodsId, v in d_shopping.datas.items():
            if v.get('shopId') == 1:
                if v.get('price') == 0:
                    oneGoods.append(v.get('goodsId'))
                if v.get('quality') == 1 or 2:
                    towGoods.append(v.get('goodsId'))
                if v.get('quality') == 3 or 4:
                    threeGoods.append(v.get('goodsId'))
        goodsIdDict = {1: oneGoods, 2: towGoods, 3: threeGoods}
    if shopId == 2:
        for goodsId, v in d_shopping.datas.items():
            if v.get('shopId') == 2:
                if v.get('quality') == 1:
                    oneGoods.append(v.get('goodsId'))
                if v.get('quality') == 2:
                    towGoods.append(v.get('goodsId'))
                if v.get('quality') == 3:
                    threeGoods.append(v.get('goodsId'))
                if v.get('quality') == 4:
                    fourGoods.append(v.get('goodsId'))
                if v.get('quality') == 5:
                    fiveGoods.append(v.get('goodsId'))
                if v.get('quality') == 6:
                    sixGoods.append(v.get('goodsId'))
        goodsIdDict = {1: oneGoods, 2: towGoods, 3: threeGoods, 4: fourGoods, 5: fiveGoods, 6: sixGoods}
    return goodsIdDict


def getEveryDayGoods():
    """
    每日商城刷新排序
    @return:
    """
    GoodsList = []
    goodsIdDict = getGoods(1)
    GoodsList.append(random.choice(goodsIdDict.get(1)))
    GoodsList.append(random.sample(goodsIdDict.get(2), 5))
    GoodsList.append(random.sample(goodsIdDict.get(3), 2))
    return GoodsList


def getChiocenessGoods():
    """
    精选商城刷新
    @return:
    """
    goodsIdDict = getGoods(2)
    chiocenessGoods = []
    for quality, goods in goodsIdDict.items():
        chiocenessGoods.append(random.choice(goods))
    return chiocenessGoods


def findGoodsInfo(goosId):
    """
    获取商品的信息
    @param goosId:
    @return:
    """
    itemId = d_shopping.datas.get(goosId).get('itemId')
    itemCount = d_shopping.datas.get(goosId).get('itemCount')
    price = d_shopping.datas.get(goosId).get('price')
    priceType = d_shopping.datas.get(goosId).get('priceType')
    quality = d_shopping.datas.get(goosId).get('quality')
    return itemId, itemCount, price, priceType, quality


def currencyShop():
    """
    货币商城
    @return:
    """
    currencyGoods = []
    m = []
    d = []
    for goodsId, v in d_shopping.datas.items():
        if v.get('shopId') == 4:
            if v.get('priceType') == 3:
                m.append(v.get('quality'))
                m.append(goodsId)
            if v.get('priceType') == 1:
                d.append(v.get('quality'))
                d.append(goodsId)


if __name__ == '__main__':
    getGoods(1)
    getEveryDayGoods()
