# -*- coding: utf-8 -*-
import datetime
import random
from copy import deepcopy
from dataclasses import dataclass, field

import GlobalConst
import MESSAGE_CODE
import TimeUtil
from KBEDebug import *
import d_shop
import d_shop_base
import items
from GOODS_BUY_STATE import TGoodsState
import time

from interfaces.GuildModule import GuildModule

_goods_info = {}
_goods_shop = {}
_goods_script = {1: "LimitGoods", 2: "LimitGoods", 3: "GoodsConfig", 4: "MultipleGoods", 5: "LimitGoods",
                 6: "GoodsConfig", 7: "LimitGoods", 8: "LimitGoods"}

_shop_script = {1: "DayShop", 2: "ChoiceShop", 3: "Shop", 4: "CurrencyShop", 5: "GiftBagShop", 6: "Shop",
                7: "ContractShop", 8: "GuildShop"}


@dataclass
class GoodsConfig:
    """普通商品"""
    # 商品id
    goodsId: int = 0
    # 商店id
    shopId: int = 0
    # 道具id
    itemId: list = field(default_factory=list)
    # 道具数量
    itemCount: list = field(default_factory=list)
    # 道具列表
    itemList: dict = field(default_factory=dict)
    # 首冲是否赠送
    isGive: int = 0
    # 首冲赠送多少
    giveCount: int = 0
    # 价格
    price: int = 0
    # 货币类型
    priceType: int = 0
    # 道具品质
    quality: int = 0
    # 权重
    weight: int = 0
    # 是否打折
    isDiscount: int = 0
    # 折扣比例
    discount: int = 0
    # 打折后价钱
    discountPrice: int = 0
    # 限购次数
    goodsLimit: int = -1

    def isBuyGoods(self, goodsBuyInfo, owner):
        if self.isDiscount == GlobalConst.DISCOUNT_GOODS:
            res, code = owner.checkItemCount(self.priceType, self.discountPrice)
            if res is False:
                return False, code

        res, code = owner.checkItemCount(self.priceType, self.price)
        if res is False:
            return False, code

        return True, 1

    def buyGoods(self, owner):
        if self.price == 0 or self.priceType == 0:
            return True
        owner.cutItem(self.priceType, self.price)
        return True

    def checkGive(self):
        if self.isGive > 0:
            return True
        else:
            return False

    def giveItem(self, **kwargs):
        """
        发放商品
        @param goodsBuyInfo:
        @param result:
        @return:
        """
        result = kwargs.get('result')
        owner = kwargs.get('owner')
        mult = 0
        if self.checkGive():
            goodsBuyInfo = kwargs.get('goodsBuyInfo')
            buyCount = goodsBuyInfo.getData(self.goodsId, 0)
            if buyCount <= 0:
                mult = self.giveCount

        for itemId, count in self.itemList.items():
            items.use_g_item(owner, itemId, count + mult)
            result(self.goodsId, itemId, count)

    def setGoodsBuyCount(self, goodsBuyInfo):
        if goodsBuyInfo is None:
            return
        goodsBuyInfo.addData('buyCount', 1)


class LimitGoods(GoodsConfig):
    """限购商品"""

    def isBuyGoods(self, goodsBuyInfo, owner):
        if goodsBuyInfo.getData('buyCount') >= self.goodsLimit:
            return False, MESSAGE_CODE.MC_BUY_OUT_MAX
        if self.isDiscount == GlobalConst.DISCOUNT_GOODS:
            res, code = owner.checkItemCount(self.priceType, self.discountPrice)
            if res is False:
                return False, code

        res, code = owner.checkItemCount(self.priceType, self.price)
        if res is False:
            return False, code

        return True, 1

    def giveItem(self, **kwargs):
        super(LimitGoods, self).giveItem(**kwargs)


class MultipleGoods(GoodsConfig):
    """返利商品（多给giveCount）"""

    def giveItem(self, **kwargs):
        """
        发放商品
        @param goodsBuyInfo:
        @param result:
        @return:
        """
        owner = kwargs.get('owner')
        result = kwargs.get('result')
        goodsBuyInfo = kwargs.get('goodsBuyInfo')
        mult = 0
        if goodsBuyInfo is not None:
            buyCount = goodsBuyInfo.getData('buyCount', 0)
            mult = self.giveCount if buyCount == 0 and self.isGive == 1 else 0

        for itemId, count in self.itemList.items():
            count += mult
            items.use_g_item(owner, itemId, count)
            result(self.goodsId, itemId, count)


class GuildGoods(GoodsConfig):
    """工会商品"""

    def isBuyGoods(self, goodsBuyInfo, owner):
        # if self.shopId == GlobalConst.GUILD_SHOP:
        #     gList = owner.refreshData.get(self.shopId).getData('goodsList')
        #     idx = gList.index(self.goodsId)
        #     if owner.guildLevel < idx + 1:
        #         return MESSAGE_CODE.MC_GUILD_GOODS_LESS

        if self.isDiscount == GlobalConst.DISCOUNT_GOODS:
            res, code = owner.checkItemCount(self.priceType, self.discountPrice)
            if res is False:
                return False, code

        res, code = owner.checkItemCount(self.priceType, self.price)
        if res is False:
            return False, code

        return True, 1



def onInit():
    for goodsId, goodsInfo in d_shop.datas.items():
        shopId = goodsInfo.get('shopId')
        itemId = list(goodsInfo.get('itemId'))
        itemCount = list(goodsInfo.get('itemCount'))
        itemList = dict(zip(goodsInfo.get('itemId'), goodsInfo.get('itemCount')))
        isGive = goodsInfo.get('isGive')
        giveCount = goodsInfo.get('giveCount')
        price = goodsInfo.get('price')
        priceType = goodsInfo.get('priceType')
        quality = goodsInfo.get('quality')
        weight = goodsInfo.get('weight')
        isDiscount = goodsInfo.get('isDiscount')
        discount = goodsInfo.get('discount')
        discountPrice = goodsInfo.get('discountPrice')
        goodsLimit = goodsInfo.get('goodsLimit')

        script = _goods_script.get(shopId, None)
        if script is None:
            continue

        scriptInst = eval(script)(goodsId=goodsId,
                                  shopId=shopId,
                                  itemId=itemId,
                                  itemCount=itemCount,
                                  isGive=isGive,
                                  giveCount=giveCount,
                                  price=price,
                                  priceType=priceType,
                                  quality=quality,
                                  weight=weight,
                                  isDiscount=isDiscount,
                                  discount=discount,
                                  discountPrice=discountPrice,
                                  itemList=itemList,
                                  goodsLimit=goodsLimit
                                  )
        _goods_info[goodsId] = scriptInst

        def initShop(shop, config):
            shop.randomCount = config.get("randomCount")
            shop.randomPrice = config.get("randomPrice")
            shop.randomPriceType = config.get("priceType")
            shop.shopId = config.get("shopId")
            if shop.randomCount != len(shop.randomPrice):
                ERROR_MSG('initShop Error shopId[%i]' % shop.shopId)
            return shop

        shopConfig = d_shop_base.datas.get(shopId)
        if shopConfig is None:
            continue

        _goods_shop.setdefault(shopId, initShop(eval(_shop_script[shopId])(), shopConfig)).addGoods(
            scriptInst)


class Shop:
    def __init__(self):
        # 商店id
        self.shopId = 0
        # 刷新价格
        self.randomPrice = []
        # 刷新价格类型
        self.randomPriceType = 0
        # 可刷新次数
        self.randomCount = 0
        self.goodsIdDict = {}
        self.weightDict = {}
        self.randomDict = {}

    def addGoods(self, goodsInfo):
        self.goodsIdDict.setdefault(goodsInfo.goodsId, goodsInfo)

    def getRandomGoods(self, owner, goodsList):
        return False

    def checkRefresh(self, shopInfo):
        return False

    def checkRandomPrice(self, owner):
        return False

    def isHandRefresh(self):
        return False

    def checkRefreshTime(self, owner):
        now_time = int(time.time())

        if TimeUtil.isAlternateDays(owner.lastLoginTime, now_time) is True:
            return True
        return False


class DayShop(Shop):
    """每日商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(DayShop, self).addGoods(goodsInfo)
        if goodsInfo.price == 0:
            self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(1, []).append(goodsInfo.weight)
        if goodsInfo.quality == 1 and goodsInfo.price != 0 or goodsInfo.quality == 2 and goodsInfo.price != 0:
            self.randomDict.setdefault(2, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(2, []).append(goodsInfo.weight)
        if goodsInfo.quality == 3 or goodsInfo.quality == 4:
            self.randomDict.setdefault(3, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(3, []).append(goodsInfo.weight)

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) > 0:
            for goodsId in goodsList:
                owner.goodsData.pop(goodsId, 0)

        info = list()
        randomDict = deepcopy(self.randomDict)
        weightDict = deepcopy(self.weightDict)
        info.extend(random.choices(self.randomDict.get(1), self.weightDict.get(1), k=1))
        for i in range(0, 6):
            randomGoods = random.choices(randomDict.get(2), weightDict.get(2), k=1)
            for goods in randomGoods:
                idx = randomDict.get(2).index(goods)
                randomDict.get(2).remove(goods)
                weightDict.get(2).remove(weightDict.get(2)[idx])
                info.append(goods)
        info.extend(random.choices(self.randomDict.get(3), self.weightDict.get(3), k=1))
        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info

    def checkRefresh(self, shopInfo):
        if shopInfo.getData('refreshNum', 0) <= 0:
            return False

        return True

    def checkRandomPrice(self, shopInfo):
        refreshNum = shopInfo.getData('refreshNum')
        return self.randomPrice[self.randomCount - refreshNum]

    def isHandRefresh(self):
        return True


class ChoiceShop(Shop):
    """精选商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(ChoiceShop, self).addGoods(goodsInfo)
        if goodsInfo.quality == 1 or goodsInfo.quality == 2 or goodsInfo.quality == 3:
            self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(1, []).append(goodsInfo.weight)
        if goodsInfo.quality == 4:
            self.randomDict.setdefault(2, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(2, []).append(goodsInfo.weight)
        return self.goodsIdDict

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) > 0:
            for goodsId in goodsList:
                owner.goodsData.pop(goodsId, 0)
        info = list()
        randomDict = deepcopy(self.randomDict)
        weightDict = deepcopy(self.weightDict)
        for i in range(0, 5):
            randomGoods = random.choices(randomDict.get(1), weightDict.get(1), k=1)
            for goods in randomGoods:
                idx = randomDict.get(1).index(goods)
                randomDict.get(1).remove(goods)
                weightDict.get(1).remove(weightDict.get(1)[idx])
                info.append(goods)
        info.extend(random.choices(self.randomDict.get(2), self.weightDict.get(2), k=1)),
        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info

    def checkRefresh(self, shopInfo):
        if shopInfo.getData('refreshNum') <= 0:
            return False

        return True

    def checkRandomPrice(self, shopInfo):
        refreshNum = shopInfo.getData('refreshNum')
        return self.randomPrice[self.randomCount - refreshNum]

    def isHandRefresh(self):
        return True


class GiftBagShop(Shop):
    """礼包"""

    def __init__(self):
        Shop.__init__(self)

    def checkLimit(self, goodsBuyInfo):
        if goodsBuyInfo.getData('buyCount') >= 1:
            return False
        return True

    def addGoods(self, goodsInfo):
        super(GiftBagShop, self).addGoods(goodsInfo)
        self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) > 0:
            for goodsId in goodsList:
                owner.goodsData.pop(goodsId, 0)
        info = list()
        info.append(random.choice(self.randomDict.get(1)))
        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info


class CurrencyShop(Shop):
    """货币商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(CurrencyShop, self).addGoods(goodsInfo)
        if goodsInfo.isGive == 1:
            self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) > 0:
            for goodsId in goodsList:
                owner.goodsData.pop(goodsId, 0)
        info = self.randomDict.get(1)
        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info


class ContractShop(Shop):
    """契约商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(ContractShop, self).addGoods(goodsInfo)
        self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) > 0:
            for goodsId in goodsList:
                owner.goodsData.pop(goodsId, 0)
        info = self.randomDict.get(1)
        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info


class GuildShop(Shop):
    """工会商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(GuildShop, self).addGoods(goodsInfo)
        if goodsInfo.quality == GlobalConst.HERO_QUALITY_N:
            self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(1, []).append(goodsInfo.weight)
        if goodsInfo.quality == GlobalConst.HERO_QUALITY_S:
            self.randomDict.setdefault(2, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(2, []).append(goodsInfo.weight)
        if goodsInfo.quality == GlobalConst.HERO_QUALITY_SR:
            self.randomDict.setdefault(3, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(3, []).append(goodsInfo.weight)
        if goodsInfo.quality == GlobalConst.HERO_QUALITY_SSR:
            self.randomDict.setdefault(4, []).append(goodsInfo.goodsId)
            self.weightDict.setdefault(4, []).append(goodsInfo.weight)

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) > 0:
            for goodsId in goodsList:
                owner.goodsData.pop(goodsId, 0)

        info = list()
        randomDict = deepcopy(self.randomDict)
        weightDict = deepcopy(self.weightDict)

        for i in range(0, 2):
            nGoods = random.choices(randomDict.get(1), weightDict.get(1), k=1)
            sGoods = random.choices(randomDict.get(2), weightDict.get(2), k=1)
            srGoods = random.choices(randomDict.get(3), weightDict.get(3), k=1)
            ssrGoods = random.choices(randomDict.get(4), weightDict.get(4), k=1)
            for goods in nGoods:
                idx = randomDict.get(1).index(goods)
                randomDict.get(1).remove(goods)
                weightDict.get(1).remove(weightDict.get(1)[idx])
                info.append(goods)
            for goods in sGoods:
                idx = randomDict.get(2).index(goods)
                randomDict.get(2).remove(goods)
                weightDict.get(2).remove(weightDict.get(2)[idx])
                info.append(goods)
            for goods in srGoods:
                idx = randomDict.get(3).index(goods)
                randomDict.get(3).remove(goods)
                weightDict.get(3).remove(weightDict.get(3)[idx])
                info.append(goods)
            for goods in ssrGoods:
                idx = randomDict.get(4).index(goods)
                randomDict.get(4).remove(goods)
                weightDict.get(4).remove(weightDict.get(4)[idx])
                info.append(goods)

        # guildLv = GuildModule.queryGuildInfo(owner)
        #
        # if guildLv < 8:
        #     info = info[0:guildLv]
        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info

    def isHandRefresh(self):
        return True

    def checkRefresh(self, shopInfo):
        return True


def getShopInfo(shopId):
    """
    获取商店信息
    @param shopId:
    @return:
    """

    return _goods_shop.get(shopId, None)


def getGoodsInfo(goodsId):
    """
    获取商品信息
    @param goodsId:
    @return:
    """
    return _goods_info.get(goodsId, None)
