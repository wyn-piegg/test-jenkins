# -*- coding: utf-8 -*-

import talent
from NODE_TALENT_NUM import NodeTalentNum


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
        talent_result = []
        talent_result.append(NodeTalentNum().createFromDict(
            {'talentNum': node.talentNum, 'totalPoints': totalPoints, 'talentCount': self.talentCount}))
        self.client.onLotteryResult(talent_result)

    def savePoint(self, treeIdx):
        """
        保存天赋点数
        @param treeIdx:
        @return:
        """

        nodeList, totalPoints = talent.findNode(treeIdx)
        talent_result = []
        for n in range(0, len(nodeList)):
            node = nodeList[n]
            talent_result.append(NodeTalentNum().createFromDict(
                {'talentNum': node.talentNum, 'totalPoints': totalPoints, 'talentCount': self.talentCount}))
        self.client.onLotteryResult(talent_result)

    def resetPoint(self, treeIdx):
        """
        重置天赋树
        @param treeIdx:
        @return:
        """
        nodeList, totalPoints = talent.findNode(treeIdx)
        self.talentCount += totalPoints
        talent_result = []
        for n in range(0, len(nodeList)):
            node = nodeList[n]
            node.talentNum = 0
            talent_result.append(NodeTalentNum().createFromDict(
                {'talentNum': node.talentNum, 'totalPoints': totalPoints, 'talentCount': self.talentCount}))
        self.client.onLotteryResult(talent_result)

    if __name__ == '__main__':
        pass








def findNode(treeIdx):
    """
    寻找天赋树上的node
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
    return nodeList, totalPoints





