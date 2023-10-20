# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from data import talent_cs

_talent_info = {}


@dataclass
class TalentConfig:
    # 天赋id
    talentId: int = 0
    # 天赋树id
    treeId: int = 0
    # 是否是终极技能
    isElementary: int = 0
    # 上一级天赋id
    parentId: list = field(default_factory=list)
    # 最大可加点数
    maxNum: int = 0
    # 初始点数
    talentNum: int = 0


def onInit():
    for talentId, talentInfo in talent_cs.datas.items():
        talentId = talentId
        treeId = talentInfo.get('treeId')
        isElementary = talentInfo.get('isElementary')
        parentId = list(talentInfo.get('parentId'))
        maxNum = talentInfo.get('maxNum')
        talentNum = talentInfo.get('talentNum')
        scriptInst = TalentConfig(talentId=talentId,
                                  treeId=treeId,
                                  isElementary=isElementary,
                                  parentId=parentId,
                                  maxNum=maxNum,
                                  talentNum=talentNum,
                                  )
        _talent_info[talentId] = scriptInst

    print(_talent_info)


def judgeIsAdd(talentId, owner):
    if judgeParent(talentId) == 0 and _talent_info.get(talentId).isElementary == 1:
        treeInfo = owner.treeData.get(_talent_info.get(talentId).treeId, None)
        if treeInfo is None:
            return False  # 树上没有点数不能添加终极技能
        if treeInfo.getData('treePoints', 0) < 20:
            return False  # 树上点数不到20不能添加终极技能
        return True
    if judgeParent(talentId) == 0 and _talent_info.get(talentId).isElementary == 0:
        talentNumInfo = owner.talentData.get(talentId, None)
        if talentNumInfo.getData('talentNum') == _talent_info.get(talentId).maxNum:
            return False  # 天赋id已达到最高点数不能再加
        return True
    if judgeParent(talentId) > 0:
        for parentId in _talent_info.get(talentId).parentId:
            talentNumInfo = owner.talentData.get(_talent_info.get(parentId), None)
            if talentNumInfo is None:
                return False  # 上一级没有添加记录故为0
            return True
#
#
# def judgeIsSave(treeId, owner):
#     for talentId, info in _talent_info.items():
#         if info.treeId == treeId:
#             talentNumInfo = owner.talentData.get(talentId, None)
#             if talentNumInfo is None:
#                 return
#             if talentNumInfo.getData('talentNum', 0) == 0:
#                 return
#             if talentNumInfo.getData('talentNum', 0) > 0:
#                 for parentId in info.parentId:
#                     talentNumInfo = owner.talentData.get(_talent_info.get(parentId), None)
#                     if talentNumInfo is None:
#                         return False  # 上一级没有添加记录故为0
#                     return True
#             treeInfo = owner.treeData.get(treeId, None)
#             if info.isElementary == 1 and treeInfo is None or treeInfo.getData('treePoints', 0) < 20:
#                 return False
#             return True


def judgeParent(talentId):
    parentList = _talent_info.get(talentId).parentId
    return len(parentList)


def findTalentInfo():
    return _talent_info


if __name__ == '__main__':
    onInit()
    print()
