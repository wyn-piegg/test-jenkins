# -*- coding: utf-8 -*-
import datetime
import random
from KBEDebug import *
import d_shopping
from interfaces import CoinModule


class shopModule:
    def __init__(self):
        self.everyDayRefreshNum = 5
        self.chiocenessRefreshNum = 5
        self.lastRefreshTime = 0

    def shopping(self, goodsId):
        """
        购买商品
        @param goodsId:
        @return:
        """
        goods_result = []
        priceType = d_shopping.datas.get(goodsId).get('priceType')
        price = d_shopping.datas.get(goodsId).get('price')
        if CoinModule.checkCoinByType(self, priceType, price) is False:
            return
        CoinModule.cutCoinHandle(self, priceType, price)

    def refresheveryDay(self,shopId):
        """
        刷新商城
        @return:
        """
        everyDayGoods = []
        if self.everyDayRefreshNum <= 0:
            return
        freeGoods = []
        middleGoods = []
        PurpleGoldGoods = []
        for k, v in d_shopping.datas.items():
            if v.get('shopId') == 1 and v.get('price') == 0:
                freeGoods.append(v.get('goodsId'))
            if v.get('shopId') == 1 and v.get('quality') == 1 or v.get('quality') == 2:
                middleGoods.append(v.get('goodsId'))
            if v.get('shopId') == 1 and v.get('quality') == 3 or v.get('quality') == 4:
                PurpleGoldGoods.append(v.get('goodsId'))
        everyDayGoods.append(random.choice(freeGoods))
        everyDayGoods.append(random.sample(middleGoods, 5))
        everyDayGoods.append(random.sample(PurpleGoldGoods, 2))
        self.everyDayRefreshNum -= 1

    def refreshChioceness(self):
        """
        刷新精选商城
        @return:
        """
        chiocenessGoods = []
        if self.chiocenessRefreshNum <= 0:
            return
        oneGoods = []
        towGoods = []
        threeGoods = []
        fourGoods = []
        fiveGoods = []
        sixGoods = []

        p2g = {6: oneGoods, 30: towGoods, 68: threeGoods}

        for k, v in d_shopping.datas.items():
            # if v.get('shopId') == 2 and v.get('price') == 6:
            #     oneGoods.append(v.get('goodsId'))
            # if v.get('shopId') == 2 and v.get('price') == 30:
            #     towGoods.append(v.get('goodsId'))
            # if v.get('shopId') == 2 and v.get('price') == 68:
            #     threeGoods.append(v.get('goodsId'))
            # if v.get('shopId') == 2 and v.get('price') == 128:
            #     fourGoods.append(v.get('goodsId'))
            # if v.get('shopId') == 2 and v.get('price') == 328:
            #     fiveGoods.append(v.get('goodsId'))
            # if v.get('shopId') == 2 and v.get('price') == 648:
            #     sixGoods.append(v.get('goodsId'))

            if v.get('shopId') == 2:
                goods = p2g.get(v.get('price'), None)
                if goods is None:
                    ERROR_MSG("goods : price" % v.get('price'))
                    continue
                goods.append(v.get('goodsId'))


        p2g = getchiocenessGoods()
        for price, goods in p2g.items():
            chiocenessGoods.append(random.choice(goods))

        # chiocenessGoods.append(random.choice(oneGoods))
        # chiocenessGoods.append(random.choice(towGoods))
        # chiocenessGoods.append(random.choice(threeGoods))
        # chiocenessGoods.append(random.choice(fourGoods))
        # chiocenessGoods.append(random.choice(fiveGoods))
        # chiocenessGoods.append(random.choice(sixGoods))
        self.chiocenessRefreshNum -= 1

    def refreshShop(self):
        """
        刷新商店
        @return:
        """
        now_time = int(datetime.datetime.now().strftime("%Y%m%d"))
        if now_time - self.lastRefreshTime < 1:
            return

        self.refresheveryDay()
        self.refreshChioceness()
        self.everyDayRefreshNum = 5
        self.lastRefreshTime = now_time
