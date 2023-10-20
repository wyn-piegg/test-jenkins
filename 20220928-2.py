# -*- coding: utf-8 -*-
import talent


class TalentModule:
    def __init__(self):
        pass
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
            return False  # 天赋id不对
        talentNumInfo = self.talentData.get(talentId, None)
        if talentNumInfo is None:
            talentNumInfo = TItemInfo().createFromDict({'talentId': talentId, 'talentNum': 0})
            self.talentDtat[talentId] = talentNumInfo
        if talent.judgeIsAdd(talentId, self) is False:
            return False  # 当前天赋不可添加点数
        self.totalPoints -= 1
        talentNumInfo.addData('talentNum', 1)
        treeInfo = self.treeData.get(talentInfo.treeId, None)
        if treeInfo is None:
            treeInfo = TItemInfo().createFromDict({'treeId': talentInfo.treeId, 'treePoints': 0})
            self.treeData[talentInfo.treeId] = treeInfo
        treeInfo.addData('treePoints', 1)
        now_talentNum = talentNumInfo.getData('talentNum', 0)
        self.client.onAddPoint(talentId, now_talentNum)

    def resetPoint(self, treeId):
        for talentId, info in talent.findTalentInfo().items():
            if info.treeId == treeId:
                talentNumInfo = self.talentData.get(talentId, None)
                if talentNumInfo is None:
                    return
                talentNumInfo.setData('talentNum', 0)
                treeInfo = self.treeData.get(treeId, None)
                if treeInfo is None:
                    return
                self.totalPoints += treeInfo.getData('treePoints', 0)

    #
    # def savePoint(self, treeId):
    #     self.addPoint(treeId)
