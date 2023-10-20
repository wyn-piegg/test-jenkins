# -*- coding: utf-8 -*-
talentInfo = talent.findTalentInfo()
for talentId, info in talentInfo.items():
    talentNumInfo = self.talentData.get(talentId, None)
    if talentNumInfo is None:
        talentNumInfo = TItemInfo().createFromDict({'talentId': talentId, 'talentNum': 0})
        self.talentDtat[talentId] = talentNumInfo
    treeInfo = self.treeData.get(info.treeId, None)
    if treeInfo is None:
        treeInfo = TItemInfo().createFromDict({'treeId': info.treeId, 'treePoints': 0})
        self.treeData[talentInfo.treeId] = treeInfo