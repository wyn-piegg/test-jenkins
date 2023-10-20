# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
from dataclasses import dataclass, field

import d_talent
from KBEDebug import ERROR_MSG

_talentTree = {}


@dataclass
class Node:
    # 树的根
    root: any
    # 树的叶
    ultimate: any
    # 点数
    talentNum: int = 0
    # 最大点数
    maxNum: int = 5
    # Node的数据
    nodeData: dict = field(default_factory=dict)
    # 上一层
    parent = None

    def __post_init__(self):
        for treeIdx, nodeList in self.nodeData.items():
            if d_talent.datas[treeIdx] is None:
                ERROR_MSG("lottery config fail heroObj is None %d" % treeIdx)
                return


def onInit():
    pass


def findParentAndPoint(treeIdx, nodeidx):
    """
    寻找上一级的天赋点数
    @param treeIdx:
    @param nodeidx:
    @return:
    """
    childTree = _talentTree.get(treeIdx)
    node = childTree.get(nodeidx)
    totalPoints = childTree['totalPoints']
    if node.root:
        return node, 1

    if node.ultimate:
        if totalPoints < 20:
            return node, 0
        else:
            return node, 1

    point = 0
    for p in node.parent:
        point += childTree[p].talentNum
    return node, point, totalPoints

