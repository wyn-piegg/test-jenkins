# -*- coding: utf-8 -*-
import talent


class TalentModule:
    def __init__(self):
        pass

    def addPoint(self, treeIdx, nodeIdx):
        """
        增加天赋点数
        @param treeIdx:
        @param nodeIdx:
        @return:
        """
        if self.talentCount < 1:
            return
        if talent.findParentAndPoint(treeIdx, nodeIdx) is False:
            return
        node, totalPoints = talent.findParentAndPoint(treeIdx, nodeIdx)

        node.talentNum += 1
        totalPoints += 1
        self.talentCount -= 1

    def savePoint(self, treeIdx, nodeIdx):
        """
        保存天赋点数
        @param treeIdx:
        @param nodeIdx:
        @return:
        """

    def resetPoint(self, treeIdx):
        """
        重置天赋树
        @param treeIdx:
        @return:
        """
        code, totalPoints = talent.clearPoint(treeIdx)
        if code is False:
            return
        self.talentCount += totalPoints


if __name__ == '__main__':
    pass



def clearPoint(treeIdx):
    """
    天赋点数清零
    @param treeIdx:
    @return:
    """
    childTree = _talentTree.get(treeIdx)
    nodeList = []
    totalPoints = 0
    for i in childTree:
        node = childTree.get(i)
        totalPoints = node.totalPoints
        nodeList.append(node)
    nlen = len(nodeList)
    for n in range(0, nlen):
        nodeList[n].talentNum = 0

    return True, totalPoints


