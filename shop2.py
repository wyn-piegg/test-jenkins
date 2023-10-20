# -*- coding: utf-8 -*-
import datetime

import GlobalConst
import MESSAGE_CODE
import guild
import shop
from KBEDebug import *
from REFRESH_SHOP import RefreshShopInfo
from SHOP_INFO import ShopInfo


class ShopModule:
    def __init__(self):
        self.refreshShop(1)
        self.refreshShop(2)
        self.refreshShop(4)
        self.refreshShop(5)
        self.refreshShop(7)

    def getGoodsData(self, goodsId):
        return self.goodsData.get(goodsId, None)

    def shopping(self, goodsId):
        """
        购买商品
        @param goodsId:
        @return:
        """
        info = shop.getGoodsInfo(goodsId)
        if info is None:
            return self.onErrorMsg(MESSAGE_CODE.MC_GOODS_LESS)

        goodsBuyInfo = self.goodsData.get(goodsId, None)

        res, code = info.isBuyGoods(goodsBuyInfo, self)
        if res is False:
            return self.onErrorMsg(code)

        shopInfo = shop.getShopInfo(info.shopId)
        if shopInfo is None:
            return self.onErrorMsg(MESSAGE_CODE.MC_SHOP_INFO_NONE)

        info.buyGoods(self)

        shop_result = []

        def result(resGoodsId, itemId, count):
            shop_result.append(ShopInfo().createFromDict(
                {'goodsId': resGoodsId, 'itemId': itemId, 'count': count}))

        info.giveItem(owner=self, goodsBuyInfo=goodsBuyInfo, result=result)
        info.setGoodsBuyCount(goodsBuyInfo)

        self.upDataTaskStatus(GlobalConst.TASK_TYPE_BUY_COUNT, 1)
        self.client.onShopping(shop_result)

    def handRefreshShop(self, shopId):
        """
        手动刷新商城
        @return:
        """
        shopInfo = shop.getShopInfo(shopId)
        if shopInfo is None:
            return self.onErrorMsg(MESSAGE_CODE.MC_SHOP_INFO_NONE)
        if shopInfo.isHandRefresh() is False:
            return self.onErrorMsg(MESSAGE_CODE.MC_SHOP_ID_LESS)

        shopObj = self.refreshData.get(shopId)
        if shopInfo.checkRefresh(shopObj) is False:
            return self.onErrorMsg(MESSAGE_CODE.MC_REFRESH_LESS)

        price = shopInfo.checkRandomPrice(shopObj)
        if price != 0:
            res, code = self.cutItem(shopInfo.randomPriceType, price)
            if res is False:
                return self.onErrorMsg(MESSAGE_CODE.MC_CURR_LESS)

        self.cutRefreshNum(shopObj, 1)
        goodsList = shopInfo.getRandomGoods(self, shopObj.getData('goodsList'))
        self.client.onHandRefresh(shopId, goodsList)

    def refreshShop(self, shopId):
        """
        定时刷新商店
        @return:
        """
        shopInfo = shop.getShopInfo(shopId)
        if shopInfo is None:
            ERROR_MSG("not find  %s this shopId error" % shopId)
            return

        if shopInfo.checkRefreshTime(self) is False:
            return

        refreshInfo = self.refreshData.get(shopId, None)
        if refreshInfo is None:
            self.refreshData[shopId] = RefreshShopInfo().createFromDict(
                {'shopId': shopId, 'refreshNum': 0, 'goodsList': []})
        if shopInfo.getRandomGoods(self, self.refreshData[shopId].getData('goodsList')) is False:
            ERROR_MSG()
            return
        self.refreshData[shopId].setData('refreshNum', shopInfo.randomCount)

    def cutRefreshNum(self, shopInfo, count):
        """
        减少刷新次数
        @param shopInfo:
        @param count:
        @return:
        """
        shopInfo.cutData('refreshNum', count)
