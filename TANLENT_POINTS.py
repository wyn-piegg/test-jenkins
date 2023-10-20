# -*- coding: utf-8 -*-
"""
@Time    : 2022/6/28 10:00
@Author  : Mgq
@File    : ITEM_INFO.py
@Software: PyCharm
@Purpose : ITEM_INFO
"""

import KBEngine
from KBEDebug import *

import CustomList
import KBEngine
from KBEDebug import *


class TalentNumInfo(CustomList.CustomList):
    def __init__(self):
        CustomList.CustomList.__init__(self)
        self.key2Data = {'talentId': 0, 'talentNum': 1}

    def asDict(self):
        data = {
            "talentId": self[0],
            "talentNum": self[1],
        }
        return data

    def createFromDict(self, dictData):
        self.extend([dictData["talentId"], dictData["talentNum"]])
        return self


class TALENT_INFO_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dictData):
        return TalentNumInfo().createFromDict(dictData)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TalentNumInfo)


talent_info_inst = TALENT_INFO_PICKLER()
