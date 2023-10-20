# -*- coding: utf-8 -*-
# from dataclasses import dataclass, field
#
# # import d_talent
#
# _talentTree = {}
#
#
# @dataclass
# class Node:
#     # 初技能
#     elementary: any = False
#     # 终极技能
#     ultimate: any = False
#     # 点数
#     talentNum: int = 0
#     # 树的总点数
#     totalPoints: int = 0
#     # 最大点数
#     maxNum: int = 5
#     # 上一层
#     parent: dict = field(default_factory=dict)
#
#     def __post_init__(self):
#         for treeIdx, nodeList in d_talent.datas.items():
#             self.parent[treeIdx] = nodeList['relation']
#             self.totalPoints = nodeList['totalPoints']
#
#
# def onInit(nodeData):
#     _node = Node()
#     for treeIdx, nodeList in _node.parent.items():
#         for key, p in nodeList.items():
#             node = _talentTree.setdefault(treeIdx, {}).setdefault(key, Node())
#             node.talentNum = nodeData.get("%s-%s" % (treeIdx, key), None)
#             node.parent = p
#             node.elementary = True if len(p) <= 0 else False
#             node.ultimate = True if len(p) == 7 else False
#
#
# def findParentAndPoint(treeIdx, nodeIdx):
#     """
#     寻找上一级的天赋点数
#     @param nodeIdx:
#     @param treeIdx:
#     @return:
#     """
#     childTree = _talentTree.get(treeIdx)
#     node = childTree.get(nodeIdx)
#     totalPoints = node.totalPoints
#     if node.elementary:
#         return node, 1
#     if node.talentNum >= node.maxNum:
#         return False
#
#     if node.ultimate:
#         if totalPoints < 20:
#             return node, 0
#         else:
#             return node, 1
#
#     parentPoint = 0
#     for p in node.parent:
#         parentPoint += childTree[p].talentNum
#     if parentPoint < 1:
#         return False
#
#     return node, totalPoints
#
#
# if __name__ == '__main__':
#     pass
#     # onInit()
#     # findParentAndPoint(1, 3)
#     # # clearPoint(1)
