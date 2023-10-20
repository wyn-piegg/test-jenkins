# -*- coding: utf-8 -*-
import talent


class TalentModule:
    def __init__(self):
        self.initPoints()
        # itemInfo = bagObj.bagData.get(itemId, None)
        # if itemInfo is None:
        #     itemInfo = TItemInfo().createFromDict({'itemId': itemId, 'count': 0})
        #     bagObj.bagData[itemId] = itemInfo
        #
        # itemInfo.addData('count', count)
        #
        # current = itemInfo.getData('count')

    def addPoint(self, talentId):
        talentInfo = talent.findTalentInfo().get(talentId)
        if talentInfo is None:
            return self.onErrorMsg(MESSAGE_CODE.MC_TALENT_ID_LESS)  # 天赋id不对
        talentNumInfo = self.talentData.get(talentId, None)
        if talentNumInfo is None:
            talentNumInfo = TItemInfo().createFromDict({'talentId': talentId, 'talentNum': 0})
            self.talentData[talent] = talentNumInfo
        if talentNumInfo.getData('talentNum') == talentInfo.maxNum:
            return self.onErrorMsg(MESSAGE_CODE.MC_TALENT_POINTS_MAX)  # 天赋已达到最大点数
        # talentNumInfo = self.talentData.get(talentId, None)
        if talentInfo.judgeIsAdd(self) is False:
            return self.onErrorMsg(MESSAGE_CODE.MC_TALENT_POINTS_LESS)  # 当前天赋不可添加点数
        treeInfo = self.treeData.get(talentInfo.treeId, None)
        if treeInfo is None:
            treeInfo = TItemInfo().createFromDict({'treeId': talentInfo.treeId, 'treePoints': 0})
            self.treeData[talentInfo.treeId] = treeInfo
        treeInfo.addData('treePoints', 1)
        self.totalPoints -= 1
        now_talentNum = talentNumInfo.getData('talentNum', 0)
        self.client.onAddPoint(talentId, now_talentNum)

    def resetPoint(self, treeId):
        self.totalPoints = 0
        for talentId, info in talent.findTalentInfo().items():
            if info.treeId == treeId:
                talentNumInfo = self.talentData.get(talentId, None)
                talentNumInfo.setData('talentNum', 0)
                treeInfo = self.treeData.get(treeId, None)
                self.totalPoints += treeInfo.getData('treePoints', 0)
        return self.totalPoints

    #
    # def savePoint(self, treeId):
    #     if talent.judgeIsSave(treeId, self) is False:
    #         return
    #     talentInfo = talent.findTalentInfo()
    #     for talentId,info in talentInfo.items():
    #         if info.treeId==treeId:
    #             talentNumInfo=self.talentData.get(talent,None):
    #             talentNumInfo.setData('talentNum',info.talentNum)

    def initPoints(self):

        return
