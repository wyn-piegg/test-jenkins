# -*- coding: utf-8 -*-

from dataclasses import dataclass
from collections import namedtuple

import MESSAGE_CODE
from KBEDebug import *
import d_chariot_info
import d_chariot_parts
import d_role_info
from PARTS_LEVEL_INFO import TPartsLevelInfo

_parts_type = {}
_parts_lv = {}
_chariot_parts_info = {}
_parts_script = {0: "ChariotConfig", 1: "ChariotParts", 2: "ChariotParts", 3: "ChariotParts", 4: "ChariotCommander"}


@dataclass
class ChariotConfig:
    # 部件id
    partsId: int = 0
    # 部件类型
    partsType: int = 0
    # 最大等级
    maxLevel: int = 0
    # 所需碎片类型
    needFrag: int = 0
    # 所需碎片数量
    needCount: int = 0
    # 等级
    lv: int = 0

    def installParts(self, owner):
        """上阵战车部件"""
        if self.partsId not in owner.chariotList:
            return False, MESSAGE_CODE.MC_CHARIOT_NO_HAVE, -1

        if owner.chariotUseParts[self.partsType] == self.partsId:
            return False, MESSAGE_CODE.MC_CHARIOT_PARTS_HAVE, -1

        owner.chariotUseParts[self.partsType] = self.partsId
        return True, MESSAGE_CODE.MC_CHARIOT_PARTS_OK, self.partsType

    def isUpLevel(self, owner):
        return False, MESSAGE_CODE.MC_CHARIOT_NO_LEVEL

    def upLevel(self, owner):
        return False

    def addPoints(self, owner, propertyIdx):
        return False, MESSAGE_CODE.MC_CHARIOT_POINTS_LESS

    def cutPoints(self, owner, propertyIdx):
        return False

    def removeParts(self, owner):
        """拆卸部件"""
        return False, MESSAGE_CODE.MC_CHARIOT_NO_REMOVE, -1, 1

    def getPartsInfoToType(self, owner):
        """
        获取战车
        @param owner:
        @return:
        """
        return TPartsLevelInfo().createFromDict({"chariotPartsId": self.partsId, "level": 1})


class ChariotParts(ChariotConfig):
    def installParts(self, owner):
        """上阵战车部件"""
        if self.partsId not in owner.partsData:
            return False, MESSAGE_CODE.MC_CHARIOT_PARTS_NO_HAVE, -1

        if owner.chariotUseParts[self.partsType] == self.partsId:
            return False, MESSAGE_CODE.MC_CHARIOT_PARTS_HAVE, -1

        owner.chariotUseParts[self.partsType] = self.partsId
        return True, MESSAGE_CODE.MC_CHARIOT_PARTS_OK, self.partsType

    def removeParts(self, owner):
        """拆卸部件"""
        owner.chariotUseParts[self.partsType] = 0

        return True, MESSAGE_CODE.MC_CHARIOT_PARTS_OK, self.partsType, owner.chariotUseParts[self.partsType]

    def isUpLevel(self, owner):
        """是否可以升级"""
        partsInfo = owner.partsData.get(self.partsId)
        lv = 0 if partsInfo is None else partsInfo.getData('level')

        partsLvInfo = _parts_lv.get(self.partsId).get(lv)

        if lv >= partsLvInfo.maxLevel:
            return False, MESSAGE_CODE.MC_CHARIOT_PARTS_MAX_LEVEL
        res, code = owner.checkItemCount(partsLvInfo.needFrags, partsLvInfo.needCount)
        return res, code

    def upLevel(self, owner):
        """给部件升级"""
        partsInfo = owner.partsData.get(self.partsId)
        lv = 0 if partsInfo is None else partsInfo.getData('level')

        partsLvInfo = _parts_lv.get(self.partsId).get(lv)
        owner.cutItem(partsLvInfo.needFrags, partsLvInfo.needCount)

        if partsInfo is None:
            partsInfo = TPartsLevelInfo().createFromDict({'chariotPartsId': self.partsId, 'level': 0})
            owner.partsData[self.partsId] = partsInfo

        partsInfo.addData('level', 1)
        return True, partsInfo.getData('level', 0)

    def addPoints(self, owner, propertyIdx):
        return False, MESSAGE_CODE.MC_CHARIOT_PARTS_POINTS_LESS

    def getPartsInfoToType(self, owner):
        partsInfo = owner.partsData.get(self.partsId)
        if partsInfo is None:
            ERROR_MSG(" getPartsInfo id %s is node " % self.partsId)
            return

        partsInfo.getData('level')
        return TPartsLevelInfo().createFromDict({"chariotPartsId": self.partsId, "level": partsInfo.getData('level')})


class ChariotCommander(ChariotConfig):
    def isUpLevel(self, owner):
        return False, MESSAGE_CODE.MC_CHARIOT_COMMANDER_NO_LEVEL

    def installParts(self, owner):
        """上阵战车部件"""
        if self.partsId not in owner.commanderData:
            return False, MESSAGE_CODE.MC_CHARIOT_COMMANDER_NO_HAVE, -1

        if owner.chariotUseParts[self.partsType] == self.partsId:
            return False, MESSAGE_CODE.MC_CHARIOT_PARTS_HAVE, -1

        owner.chariotUseParts[self.partsType] = self.partsId
        return True, MESSAGE_CODE.MC_CHARIOT_PARTS_OK, self.partsType

    def addPoints(self, owner, propertyIdx):
        """是否可以加点"""
        commanderInfo = owner.commanderData.get(self.partsId)

        if sum(commanderInfo.getData('propertyList')) == owner.level:
            return False, MESSAGE_CODE.MC_CHARIOT_COMMANDER_MAX_POINTS

        """给属性加点"""
        commanderInfo = owner.commanderData.get(self.partsId)

        commanderInfo.getData('propertyList')[propertyIdx] += 1
        return True, MESSAGE_CODE.MC_CHARIOT_COMMANDER_OK

    def cutPoints(self, owner, propertyIdx):
        """属性减点"""
        commanderInfo = owner.commanderData.get(self.partsId)
        points = commanderInfo.getData('propertyList')[propertyIdx]
        points -= 1
        if points < 0:
            return False
        commanderInfo.getData('propertyList')[propertyIdx] = points
        return True

    def removeParts(self, owner):
        """拆卸部件"""
        return False, MESSAGE_CODE.MC_CHARIOT_COMMANDER_NO_REMOVE, -1, 1

    def getPartsInfoToType(self, owner):
        return super(ChariotCommander, self).getPartsInfoToType(owner)


def onInit():
    for _id, chariotInfo in d_chariot_parts.datas.items():
        partsId = int(_id.split("_")[0])
        lv = int(_id.split("_")[1])
        partsType = chariotInfo.get('partsType')
        maxLevel = chariotInfo.get('maxLevel')
        needFrag = chariotInfo.get('needFrag')
        needCount = chariotInfo.get('needCount')
        partsLv = namedtuple('partsLv', ['lv', 'needFrags', 'needCount', 'maxLevel'])
        _parts_lv.setdefault(partsId, {})[lv] = partsLv(lv, needFrag, needCount, maxLevel)

        script = _parts_script.get(partsType, None)
        scriptInst = eval(script)(partsId=partsId,
                                  partsType=partsType,
                                  )

        _chariot_parts_info[partsId] = scriptInst
        _parts_type.setdefault(partsType, []).append(partsId)

    for partsId, chariotInfo in d_chariot_info.datas.items():
        partsType = chariotInfo.get('partsType')
        script = _parts_script.get(partsType, None)
        scriptInst = eval(script)(partsId=partsId,
                                  partsType=partsType,
                                  )
        _chariot_parts_info[partsId] = scriptInst
        _parts_type.setdefault(partsType, []).append(partsId)

    for partsId, chariotInfo in d_role_info.datas.items():
        partsType = chariotInfo.get('partsType')
        script = _parts_script.get(partsType, None)
        scriptInst = eval(script)(partsId=partsId,
                                  partsType=partsType,
                                  )
        _chariot_parts_info[partsId] = scriptInst
        _parts_type.setdefault(partsType, []).append(partsId)


def getPartsInfo(partsId):
    return _chariot_parts_info.get(partsId)


def getPartsLvInfo(partsId):
    return _parts_lv.get(partsId)


if __name__ == '__main__':
    onInit()
    info = getPartsInfo(150001)

    linfo = _parts_lv.get(150003).get(12)

    print(linfo.lv)
