# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# TalentModule

import random

import d_talent
import talent


class TalentModule:
    def __init__(self):
        pass

    def add(self, treeIdx, nodeidx):
        """
        增加天赋
        @param treeIdx:
        @param nodeidx:
        @return:
        """
        addPoint(self, treeIdx, nodeidx)


def addPoint(treeIdx, nodeidx, talentCount):
    """
    增加天赋
    @param treeIdx:
    @param nodeidx:
    @param talentCount:
    @return:
    """
    if talentCount < 1:
        return

    node, parentPoint, totalPoints = talent.findParentAndPoint(treeIdx, nodeidx)
    if node.talentNum >= node.maxNum:
        return

    if parentPoint < 1:
        return

    node.talentNum += 1
    totalPoints += 1
    talentCount -= 1
