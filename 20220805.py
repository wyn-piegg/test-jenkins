# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random

import d_talent


class Node:
    def __init__(self):
        self.root = False
        self.talentNum = 0
        self.maxNum = 5
        self.parent = None
        self.skillId = 1000
        self.ultimate = False

class TalentModule:
    def __init__(self):
        self.talentTree = {}

    def initTree(self):
        for treeIdx, nodeList in d_talent.datas.items():
            for key, p in nodeList.items():
                node = self.talentTree.setdefault(treeIdx, {}).setdefault(key, Node())
                node.talentNum = random.randint(1, 5)
                node.parent = p
                node.root = True if len(p) <= 0 else False
                node.ultimate = True if len(p) == 7 else False

    def findParentAndPoint(self, treeIdx, nodeidx):
        """
        寻找上一级的天赋点数
        @param treeIdx:
        @param nodeidx:
        @return:
        """
        childTree = self.talentTree.get(treeIdx)
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

    def addPoint(self, treeIdx, nodeidx, talentCount):
        """
        增加天赋
        @param treeIdx:
        @param nodeidx:
        @param talentCount:
        @return:
        """
        if talentCount < 1:
            return

        node, parentPoint, totalPoints = self.findParentAndPoint(treeIdx, nodeidx)

        if parentPoint < 1:
            return

        if node.talentNum >= node.maxNum:
            return

        node.talentNum += 1
        totalPoints += 1
        talentCount -= 1
