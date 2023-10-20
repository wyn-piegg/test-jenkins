# -*- coding: utf-8 -*-
# 保存
nodeList, totalPoints = talent.findNode(treeIdx)
talent_result = []
for n in range(0, len(nodeList)):
    if self.addPoint(treeIdx, n) is False:
        return
    node = nodeList[n]
    self.addPoint(treeIdx, n)
    nodeInfo = self.nodeData.get("%s-%s" % (treeIdx, n), None)
    if nodeInfo is None:
        nodeInfo = nodeNumInfo().createFromDict({'nodeIdx': "%s-%s" % (treeIdx, n), 'talentNum': 0})
        self.nodeData["%s-%s" % (treeIdx, n)] = nodeInfo
    nodeInfo.addData('talentNum', node.talentNum)
    talentNum = nodeInfo.getData('talentNum')
    talent_result = [nodeNumInfo().createFromDict(
        {'talentNum': talentNum, 'leftPoint': self.leftPoint})]
self.client.onSaveResult(talent_result)
# 重置
nodeList, totalPoints = talent.findNode(treeIdx)
self.leftPoint += totalPoints
talent_result = []
for n in range(0, len(nodeList)):
    node = nodeList[n]
    nodeInfo = self.nodeData.get("%s-%s" % (treeIdx, n), None)
    if nodeInfo is None:
        return False
    nodeInfo.cutData('talentNum', node.talentNum)
    talentNum = nodeInfo.getData('talentNum')
    talent_result.append(nodeNumInfo().createFromDict(
        {'talentNum': talentNum, 'leftPoint': self.leftPoint}))
self.client.onResetResult(talent_result)





# talent 初始化的包获取所有node

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






