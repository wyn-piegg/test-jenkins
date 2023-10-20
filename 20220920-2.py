# -*- coding: utf-8 -*-
import datetime

import shop
from GLOBAL_DICT import TGlobalList
from GOODS_BUY_STATE import TGoodsState
from KBEDebug import *
from SHOP_INFO import ShopInfo
from interfaces import CoinModule, BagModule


class ShopModule:
    def __init__(self):
        pass

    def shopping(self, goodsId):
        """
        购买商品
        @param goodsId:
        @return:
        """
        shop_result = []
        info = shop._goods_info.get(goodsId)
        goodsBuyInfo = self.goodsData.get(goodsId, None)
        if info.checkLimit(goodsBuyInfo) is False:
            return
        if CoinModule.checkCoinByType(self, info.priceType, info.price) is False:
            return
        CoinModule.cutCoinHandle(self, info.priceType, info.price)
        info.setGoodsBuyCount(goodsBuyInfo)
        itemCount = info.giveItem(goodsBuyInfo)
        info.setGoodsState(goodsBuyInfo)
        BagModule.addItemHandle(self, info.itemId, itemCount)
        shop_result.append(ShopInfo().createFromDict(
            {'itemId': info.itemId, 'count': itemCount}))
        self.client.onShopping(shop_result)

    def refresheveryDay(self):
        """
        刷新每日商城
        @return:
        """
        everyDayGoodsResult = []
        if self.everyDayRefreshNum <= 0:
            return

        everyDayGoods = shop.getDayGoods()
        self.everyDayRefreshNum -= 1
        self.everyDayGoodsList = everyDayGoods
        goodsData = TGlobalList()
        for goodsId in self.everyDayGoodsList:
            goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
            info = shop._goods_info.get(goodsId)
            everyDayGoodsResult.append(ShopInfo().createFromDict(
                {'itemId': info.itemId, 'count': info.itemCount}))
        self.client.onRefreshDayShop(everyDayGoodsResult)

    def refreshChioceness(self):
        """
        刷新精选商城
        @return:
        """
        if self.chiocenessRefreshNum <= 0:
            return

        chiocenessGoods = shop.getChiocenessGoods()
        ChiocenessGoodsResult = []
        self.chiocenessRefreshNum -= 1
        self.chiocenessGoodsList = chiocenessGoods
        goodsData = TGlobalList()
        for goodsId in self.chiocenessGoodsList:
            goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
            info = shop._goods_info.get(goodsId)
            ChiocenessGoodsResult.append(ShopInfo().createFromDict(
                {'itemId': info.itemId, 'count': info.itemCount}))
        self.client.onRefreshChioceShop(ChiocenessGoodsResult)

    def refreshShop(self):
        """
        定时刷新商店
        @return:
        """

        everyDayGoodsResult = []
        chiocenessGoodsResult = []

        now_time = int(datetime.datetime.now().strftime("%Y%m%d"))
        if now_time == self.lastRefreshTime:
            return

        self.everyDayGoodsList = shop.getDayGoods()
        self.chiocenessGoodsList = shop.getChiocenessGoods()

        self.lastRefreshTime = now_time
        goodsData = TGlobalList()
        for goodsId in self.everyDayGoodsList + self.chiocenessGoodsList:
            goodsData[goodsId] = TGoodsState().createFromDict({'goodsId': goodsId, 'buyCount': 0})
            info = shop._goods_info.get(goodsId)
            goodsResult = everyDayGoodsResult if info.shopId == 1 else chiocenessGoodsResult
            goodsResult.append(ShopInfo().createFromDict(
                {'itemId': info.itemId, 'count': info.itemCount}))


        self.goodsData = goodsData

        self.everyDayRefreshNum = 5
        self.chiocenessRefreshNum = 5
        self.client.onRefreshShop(everyDayGoodsResult, chiocenessGoodsResult)
