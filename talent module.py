# -*- coding: utf-8 -*-
import GlobalConst
import talent
from NODE_NUM import nodeNumInfo
from NODE_TALENT_NUM import NodeTalentNum


class TalentModule:
    def __init__(self):
        self.talentCount = 10
        talentNum = 0
        for k, v in self.nodeData.items():
            talentNum += v.get('talentNum')
        self.leftPoint = self.talentCount - talentNum

    def addPoint(self, treeIdx, nodeIdx):
        """
        增加天赋点数
        @param treeIdx:
        @param nodeIdx:
        @return:
        """
        if self.leftPoint < 1:
            return
        if talent.findParentAndPoint(treeIdx, nodeIdx) is False:
            return

        node, totalPoints = talent.findParentAndPoint(treeIdx, nodeIdx)
        node.talentNum += 1
        totalPoints += 1
        self.talentCount -= 1
        talent_result = [nodeNumInfo().createFromDict(
            {'talentNum': node.talentNum, 'leftPoint': self.leftPoint})]

        self.client.onAddResult(talent_result)
        return True

    def savePoint(self, treeIdx, nodeIdx):
        """
        保存天赋点数
        @param nodeIdx:
        @param treeIdx:
        @return:
        """
        if self.addPoint(treeIdx, nodeIdx) is False:
            return
        childTree = talent._talentTree.get(treeIdx)
        node = childTree.get(nodeIdx)
        talentNum = node.talentNum
        nodeInfo = self.nodeData.get("%s-%s" % (treeIdx, nodeIdx), None)
        if nodeInfo is None:
            nodeInfo = nodeNumInfo().createFromDict({'nodeIdx': "%s-%s" % (treeIdx, nodeIdx), 'talentNum': 0})
            self.nodeData["%s-%s" % (treeIdx, nodeIdx)] = nodeInfo
        nodeInfo.setData('talentNum', talentNum)
        talent_result = [nodeNumInfo().createFromDict(
            {'talentNum': talentNum, 'leftPoint': self.leftPoint})]
        self.client.onAddResult(talent_result)

    def resetPoint(self, treeIdx, nodeIdx):
        """
        重置天赋树
        @param nodeIdx:
        @param treeIdx:
        @return:
        """
        childTree = talent._talentTree.get(treeIdx)
        node = childTree.get(nodeIdx)
        totalPoints = node.totalPoints
        self.leftPoint += totalPoints
        nodeInfo = self.nodeData.get("%s-%s" % (treeIdx, nodeIdx), None)
        if nodeInfo is None:
            return
        nodeInfo.cutData('talentNum', node.talentNum)
        talentNum = nodeInfo.getData('talentNum')
        talent_result = [nodeNumInfo().createFromDict(
            {'talentNum': talentNum, 'leftPoint': self.leftPoint})]
        self.client.onResetResult(talent_result)

    def operateTalentTree(self, treeIdx, nodeIdx, operateType):
        """
        操作天赋树
        @param treeIdx:
        @param nodeIdx:
        @param operateType:
        @return:
        """
        talent_result = []
        talentObj = eval("{'talentNum': talentNum, 'talentCount': self.talentCount}")
        if operateType == GlobalConst.TALENT_TREE_ADD:
            if self.talentCount < 1:
                return
            if talent.findParentAndPoint(treeIdx, nodeIdx) is False:
                return
            node, totalPoints = talent.findParentAndPoint(treeIdx, nodeIdx)
            talentNum = node.talentNum
            talentNum += 1
            totalPoints += 1
            self.talentCount -= 1
            talent_result.append(NodeTalentNum().createFromDict(talentObj))
        elif operateType == GlobalConst.TALENT_TREE_SAVE:
            nodeList, totalPoints = talent.findNode(treeIdx)
            for n in range(0, len(nodeList)):
                node = nodeList[n]
                talentNum = node.talentNum
                if node.talentNum == 0:
                    return
                nodeInfo = self.nodeData.get("%s-%s" % (treeIdx, n), None)
                if nodeInfo is None:
                    nodeInfo = nodeNumInfo().createFromDict({'nodeIdx': "%s-%s" % (treeIdx, n), 'talentNum': 0})
                    self.nodeData["%s-%s" % (treeIdx, n)] = nodeInfo
                nodeInfo.setData('talentNum', talentNum)
                talent_result.append(NodeTalentNum().createFromDict(talentObj))
        elif operateType == GlobalConst.TALENT_TREE_RESET:
            nodeList, totalPoints = talent.findNode(treeIdx)
            self.talentCount += totalPoints
            totalPoints = 0
            for n in range(0, len(nodeList)):
                node = nodeList[n]
                nodeInfo = self.nodeData.get("%s-%s" % (treeIdx, n), None)
                if nodeInfo is None:
                    return False
                nodeInfo.cutData('talentNum', node.talentNum)
                del self.nodeData["%s-%s" % (treeIdx, n)]
                talentNum = node.talentNum = 0
                talent_result.append(NodeTalentNum().createFromDict(talentObj))
        else:
            return
        self.client.onTalentResult(talent_result)


if __name__ == '__main__':
    pass
