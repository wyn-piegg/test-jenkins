# -*- coding: utf-8 -*-
import copy
import time

import GlobalConst
from interfaces import CoinModule


class shopModule:
    def __init__(self):
        self.refreshNum = 5

    def everyDayShopping(self, idx):
        """
        每日商城
        @return:
        """
        if self.shopping[idx] == 0:
            return
        self.shopping[idx] = 1
        shop_result = []
        if idx == 0:
            return
        sList = len(self.shopping)
        for idx in range(sList):
            if sList[idx] != 1:
                return
            sList[idx] = 0

    def choiceShopping(self):
        """
        精选商城
        @return:
        """

    def vipShopping(self):
        """
        会员商城
        @return:
        """

    def currencyShopping(self):
        """
        货币商城
        @return:
        """

    def refreshShopping(self):
        """
        刷新商城
        @return:
        """
        if self.refreshNum <= 0:
            return
        res, code = CoinModule.checkCoinByType(self, GlobalConst.DIAMOND_TYPE, 5)
        while True:
            shopping = []
            time_now = time.strftime("%H:%M", time.localtime())
            if time_now == "00:00" or res is True:
                pass
