# -*- coding: utf-8 -*-
def currencyShop():
    """
    货币商城
    :return:
    """
    currencyGoods = []
    for goodsId, goodsIfo in _goods_info.items():
        if goodsIfo.shopId == 4:
            currencyGoods.append(goodsId)
