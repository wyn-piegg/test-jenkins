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

_goods_info = {}
_goods_shop = {}
_goods_script = {
    GlobalConst.LIMIT_GOODS: "LimitGoods",
    GlobalConst.RIGHT_GOODS: "GoodsConfig",
    GlobalConst.REBATE_GOODS: "MultipleGoods",
    GlobalConst.MISSION_GIFT_GOODS: "MissionGift",
    GlobalConst.MISSION_SGIFT_GOODS: "MissionSGift",
    GlobalConst.MISSION_DGIFT_GOODS: "MissionDGift",
    GlobalConst.MUST_DAILY_GOODS: "MustBuyGoods",
    GlobalConst.FIRST_PAY_GOODS: "FirstPayGoods",
    GlobalConst.FIRST_FUND_GOODS: "FundGoods",
    GlobalConst.CONTRACT_GOODS: "ContractGoods",
    GlobalConst.REPETITION_BUY_GOODS: "RepetitionBuyGoods",
}

_shop_script = {
    GlobalConst.EVERYDAY_SHOP: "DayShop",
    GlobalConst.CHIOCENESS_SHOP: "ChoiceShop",
    GlobalConst.VIP_SHOP: "Shop",
    GlobalConst.CURRENCY_SHOP: "CurrencyShop",
    GlobalConst.GIFT_BAG_SHOP: "GiftBagShop",
    GlobalConst.ITEM_SHOP: "Shop",
    GlobalConst.CONTRACT_SHOP: "ContractShop",
    GlobalConst.GUILD_SHOP: "GuildShop",
    GlobalConst.MISSION_SHOP: "MissionShop",
    GlobalConst.MUST_DAILY_SHOP: "MustDayShop",
    GlobalConst.FIRST_PAY_SHOP: "Shop",
    GlobalConst.ACTIVITY_SHOP: "Shop",
    GlobalConst.REPETITION_BUY_SHOP: "RepetitionBuyShop",
}


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
    # 商品类型
    goodsType: int = 0

    def isBuyGoods(self, goodsBuyInfo, owner):
        return True, 1

    def buyGoods(self, **kwargs):
        owner = kwargs.get("owner")
        if self.price == 0 or self.priceType == 0:
            return True, None

        res, code = owner.checkItemCount(self.priceType, self.getPrice())
        if res is False:
            return res, code

        return owner.cutItem(self.priceType, self.getPrice())

    def checkGive(self):
        if self.isGive > 0:
            return True
        else:
            return False

    def getPrice(self):
        if self.isDiscount > 0:
            return self.discountPrice
        return self.price

    def giveItem(self, **kwargs):
        """
        发放商品
        @param goodsBuyInfo:
        @param result:
        @return:
        """
        result = kwargs.get('result')
        owner = kwargs.get('owner')
        for itemId, count in self.itemList.items():
            owner.useItem(itemId, count, source=items.ItemSource.shop, result=result)
            # result(itemId=itemId, count=count)

    def setGoodsBuyCount(self, goodsBuyInfo):
        if goodsBuyInfo is None:
            return
        goodsBuyInfo.addData('buyCount', 1)


class LimitGoods(GoodsConfig):
    """限购商品"""

    def isBuyGoods(self, goodsBuyInfo, owner):
        if goodsBuyInfo is None:
            return False, MESSAGE_CODE.MC_GOODS_LESS

        if goodsBuyInfo.getData('buyCount') >= self.goodsLimit:
            return False, MESSAGE_CODE.MC_BUY_OUT_MAX

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
            owner.useItem(itemId, count, source=items.ItemSource.shop, result=result)
            # result(self.goodsId, itemId, count)


class MissionGift(GoodsConfig):
    """战令VIP商品"""
    giftLevel: int = GlobalConst.MISSION_VIP

    def isBuyGoods(self, goodsBuyInfo, owner):
        missionVip = owner.getMissionVip()
        if missionVip >= self.giftLevel:
            return False, MESSAGE_CODE.MC_CONTRACT_MISSION_VIP_ERROR

        return True, None

    def giveItem(self, **kwargs):
        owner = kwargs.get('owner')
        for itemId, count in self.itemList.items():
            owner.useItem(itemId, count, source=items.ItemSource.shop)


class MissionSGift(MissionGift):
    """战令高级礼包"""
    giftLevel: int = GlobalConst.MISSION_SVIP

    def isBuyGoods(self, goodsBuyInfo, owner):
        missionVip = owner.getMissionVip()
        if missionVip > 0:
            return False, MESSAGE_CODE.MC_CONTRACT_MISSION_SVIP_ERROR

        return True, None


class MissionDGift(MissionGift):
    """战令高级差价礼包"""
    giftLevel: int = GlobalConst.MISSION_SVIP

    def isBuyGoods(self, goodsBuyInfo, owner):
        missionVip = owner.getMissionVip()
        if missionVip != GlobalConst.MISSION_VIP:
            return False, MESSAGE_CODE.MC_CONTRACT_MISSION_DVIP_ERROR

        return True, None


class MustBuyGoods(LimitGoods):
    """每日必购商品"""

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
            owner.useItem(itemId, count + mult, source=items.ItemSource.shop, result=result, goodsId=self.goodsId)


class FirstPayGoods(GoodsConfig):
    """首冲商品"""

    def isBuyGoods(self, goodsBuyInfo, owner):
        if owner.firstPayTime != 0:
            return False, MESSAGE_CODE.MC_NOT_FIRST_PAY

        if self.price == 0 or self.priceType == 0:
            return True, 1

        if self.isDiscount == GlobalConst.DISCOUNT_GOODS:
            res, code = owner.checkItemCount(self.priceType, self.discountPrice)
            if res is False:
                return False, code

        res, code = owner.checkItemCount(self.priceType, self.price)
        if res is False:
            return False, code

        return True, 1

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
            owner.useItem(itemId, count + mult, source=items.ItemSource.shop, result=result)


class ContractGoods(GoodsConfig):
    """契约商品"""

    def buyGoods(self, **kwargs):
        owner = kwargs.get("owner")
        goodsCount = kwargs.get("goodsCount")

        if self.price == 0 or self.priceType == 0:
            return True, None

        res, code = owner.checkItemCount(self.priceType, self.getPrice() * goodsCount)
        if res is False:
            return res, code

        return owner.cutItem(self.priceType, self.getPrice() * goodsCount)

    def isBuyGoods(self, goodsBuyInfo, owner):

        if TimeUtil.getMday() >= 29:
            return False, MESSAGE_CODE.MC_CONTRACT_GOODS_LESS

        return True, 1

    def giveItem(self, **kwargs):
        """
        发放商品
        @param goodsBuyInfo:
        @param result:
        @return:
        """
        result = kwargs.get('result')
        owner = kwargs.get('owner')
        goodsCount = kwargs.get('goodsCount')

        for itemId, count in self.itemList.items():
            owner.useItem(itemId, count * goodsCount, source=items.ItemSource.shop, result=result)
            # result(itemId=itemId, count=count)


class RepetitionBuyGoods(ContractGoods):
    def isBuyGoods(self, goodsBuyInfo, owner):
        return True, 1


class FundGoods(GoodsConfig):
    """战令高级差价礼包"""
    giftLevel: int = GlobalConst.MISSION_SVIP

    def isBuyGoods(self, goodsBuyInfo, owner):
        if owner.fundUnlock > 0:
            return False

        return True, None

    def giveItem(self, **kwargs):
        """
        发放商品
        @param goodsBuyInfo:
        @param result:
        @return:
        """
        owner = kwargs.get('owner')
        for itemId, count in self.itemList.items():
            owner.useItem(itemId, count, source=items.ItemSource.shop)


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
        goodsType = goodsInfo.get('goodsType')

        script = _goods_script.get(goodsType, None)
        if script is None:
            ERROR_MSG('shop good init goodType error goodsType:[%i]' % goodsType)
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
                                  goodsLimit=goodsLimit,
                                  goodsType=goodsType
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
        shopScript = _shop_script.get(shopId)
        if shopConfig is None:
            ERROR_MSG(" d_shop_base.datas.get(%s) is None" % shopId)
            continue

        if shopScript is None:
            ERROR_MSG(" _shop_script.datas.get(%s) is None" % shopId)
            continue

        _goods_shop.setdefault(shopId, initShop(eval(shopScript)(), shopConfig)).addGoods(scriptInst)


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

    def isShopBuy(self):
        return True, None

    def isRepetitionBuy(self):
        return False

    def ifRefresh(self, owner):
        now_time = int(time.time())

        if TimeUtil.isAlternateDays(owner.lastLoginTime, now_time) is True:
            return True

        return False

    def checkRefresh(self, shopInfo):
        return False

    def checkRandomPrice(self, owner):
        return False

    def isHandRefresh(self):
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
        if len(goodsList) <= 0:
            goodsList = self.randomDict.get(1)

        for goodsId in goodsList:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', goodsList)

        return goodsList

    def isRepetitionBuy(self):
        return True


class MustDayShop(Shop):
    """每日必购商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(MustDayShop, self).addGoods(goodsInfo)
        self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)

    def getRandomGoods(self, owner, goodsList):

        if len(goodsList) <= 0:
            goodsList = self.randomDict.get(1)

        for goodsId in goodsList:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', goodsList)

        return goodsList


class RepetitionBuyShop(Shop):
    """多次购买商店"""

    def __init__(self):
        Shop.__init__(self)

    def addGoods(self, goodsInfo):
        super(RepetitionBuyShop, self).addGoods(goodsInfo)
        self.randomDict.setdefault(1, []).append(goodsInfo.goodsId)

    def getRandomGoods(self, owner, goodsList):
        if len(goodsList) <= 0:
            goodsList = self.randomDict.get(1)

        for goodsId in goodsList:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', goodsList)

        return goodsList

    def isRepetitionBuy(self):
        return True


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

        for goodsId in info:
            owner.goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
        owner.refreshData[self.shopId].setData('goodsList', info)
        return info

    def ifRefresh(self, owner):
        now_time = int(time.time())

        if TimeUtil.isAlternateDays(owner.lastLoginTime, now_time) is True:
            return True

        if owner.refreshData.get(GlobalConst.GUILD_SHOP) is None:
            return True

        return False


class MissionShop(Shop):
    """战令商店"""

    def __init__(self):
        Shop.__init__(self)


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


if __name__ == '__main__':
    print(_goods_shop)
