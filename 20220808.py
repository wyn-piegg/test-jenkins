# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# d_talent __init__


import random

import d_talent

_talentTree = {}


class Node:
    def __init__(self):
        self.root = False
        self.talentNum = 0
        self.maxNum = 5
        self.parent = None
        self.skillId = 1000
        self.ultimate = False


def initTree():
    for treeIdx, nodeList in d_talent.datas.items():
        for key, p in nodeList.items():
            node = _talentTree.setdefault(treeIdx, {}).setdefault(key, Node())
            node.talentNum = random.randint(1, 5)
            node.parent = p
            node.root = True if len(p) <= 0 else False
            node.ultimate = True if len(p) == 7 else False


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


class Grid:
    ol: list
    idx: int
    type_: int

    def delete(self):
        for n in [l, r, t, b]:
            del ol[idx]

    def change(self):
        self.type_ = 0


l = [2, 1, 3, 2, 1, 3]
m = {0: grid(idx=0, left=-1, r=1, t=-1, b=2, num=2),
     1: grid(idx=1, l=2, r=3, t=-1, b=1, num=1),
     2: grid(idx=2, l=1, r=3, t=-1, b=1, num=1),
     3: grid(idx=3, l=2, r=3, t=-1, b=1, num=1),
     4: grid(idx=4, l=2, r=3, t=-1, b=1, num=1),
     }
