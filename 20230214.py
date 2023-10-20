# -*- coding: utf-8 -*-
import time

import box
import key
import items
import serverconst
import MESSAGE_CODE
from GLOBAL_DICT import TGlobalList
from HATCH_BOX_LIST import HatchBoxInfo
from ITEM_INFO import TItemInfo
import TimeUtil


class BoxModule:
    def __init__(self):
        pass

    def hatchBox(self, boxId, idx):
        """添加宝箱进行孵化"""
        if idx > 2:
            return False, MESSAGE_CODE.MC_HATCH_NOT_LIST

        if self.hatchBoxList[idx] != 0:
            return False, MESSAGE_CODE.MC_HATCH_LIST_LESS

        itemCpt = items.get_g_items(boxId)
        if itemCpt.canOpen() is False:
            return False, MESSAGE_CODE.MC_HATCH_BOX_LESS

        res, code = self.checkItemCount(boxId, 1)
        if res is False:
            return False, code

        self.cutItem(boxId, 1)

        self.hatchBoxList[idx] = boxId
        info = box.getBoxInfo(boxId)
        self.hatchBoxInfo.createFromDict()

        self.hatchBoxInfo[idx].createFromDict({"boxId": boxId, "hTime": info.hatchTime + TimeUtil.second()})
        print(self.hatchBoxInfo)
        print(self.hatchBoxInfo[idx])

        self.hatchBoxTimeList[idx] = info.hatchTime + TimeUtil.second()

        return self.client.onHatchBox(idx, boxId, self.hatchBoxTimeList[idx])

    def speedOpenBox(self, idx, itemList, itemCountList):
        """加速开启宝箱"""
        if self.hatchBoxList[idx] == 0:
            return False, MESSAGE_CODE.MC_NOT_HATCH_BOX

        if self.hatchBoxTimeList[idx] == 0:
            return False, MESSAGE_CODE.MC_OPEN_HATCH_BOX

        itemInfo = dict(zip(itemList, itemCountList))

        speedTime = 0

        for itemId, count in itemInfo.items():
            self.useItem(itemId, count, source=items.ItemSource.hatchBox)
            info = key.getKeyInfo(itemId)

            speedTime += int(info.speedTime) * count

        openTime = int(self.hatchBoxTimeList[idx])

        self.hatchBoxTimeList[idx] = openTime - speedTime

        sTime = int(self.hatchBoxTimeList[idx]) - int(time.time())

        if sTime < 0:
            sTime = 0

        return self.client.onSpeedOpenBox(idx, sTime)

    def openBox(self, idx):
        """开宝箱"""

        boxId = self.hatchBoxList[idx]
        if boxId == 0:
            return False, MESSAGE_CODE.MC_NOT_HATCH_BOX

        if TimeUtil.second() < self.hatchBoxTimeList[idx]:
            return False, MESSAGE_CODE.MC_HATCH_BOX_NOT_TIME

        hatchReward = TGlobalList()

        def result(itemId):
            if hatchReward.get(itemId) is None:
                hatchReward[itemId] = TItemInfo().createFromDict({"itemId": itemId, "count": 1})
                return
            hatchReward[itemId].addData("count", 1)

        itemInst = items.get_g_items(boxId)
        if itemInst.canOpen() is False:
            return False, MESSAGE_CODE.MC_HATCH_BOX_LESS

        itemInst.open(source=items.ItemSource.hatchBox, result=result, owner=self)

        self.hatchBoxList[idx] = 0
        self.hatchBoxTimeList[idx] = 0

        return self.client.onOpenHatchBox(idx, hatchReward)


if __name__ == '__main__':
    serverconst.onInit()
    print(serverconst.game_const_.hangMaxTime)
