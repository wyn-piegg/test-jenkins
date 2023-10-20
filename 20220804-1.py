# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random

parent = {1: {'totalPoints': (),
              1: (),
              2: (1,),
              3: (1,),
              4: (2, 3),
              5: (2, 3),
              6: (4, 5),
              7: (6,), },
          2: {'totalPoints': (),
              1: (),
              2: (1,),
              3: (2,),
              4: (2,),
              5: (3, 4),
              6: (3, 4),
              7: (5, 6)},
          3: {
              'totalPoints': (),
              1: (),
              2: (1,),
              3: (1,),
              4: (2, 3),
              5: (4,),
              6: (4,),
              7: (5, 6)
          }
          }


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
        for treeIdx, nodeList in parent.items():
            for key, p in nodeList.items():
                node = self.talentTree.setdefault(treeIdx, {}).setdefault(key, Node())
                node.talentNum = random.randint(1, 5)
                node.parent = p
                node.root = True if len(p) <= 0 else False
                node.ultimate = True if len(p) == 7 else False

    def findParentAndPoint(self, treeIdx, nodeidx):
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

        parentPoint = 0
        for p in node.parent:
            parentPoint += childTree[p].talentNum
        return node, parentPoint, totalPoints

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
        talentCount -= 1
        totalPoints += 1
