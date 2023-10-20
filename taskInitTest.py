# -*- coding: utf-8 -*-
import random

import d_success_reward
import d_task, d_task_box
from KBEDebug import *
from dataclasses import dataclass, field

_taskDict = {}
_task_info = {}
_s_type_task_dict = {}
_task_update_type = {}
_task_refresh_type = {}
_box_info = {}
_success_reward_info = {}


@dataclass
class TaskConfig:
    # 任务ID
    taskId: int = 0
    # 任务列表ID
    taskTypeId: int = 0
    # 奖励列表
    itemId: list = field(default_factory=list)
    # 奖励数量列表
    itemCount: list = field(default_factory=list)
    # 道具列表
    itemList: dict = field(default_factory=dict)
    # 任务类型
    taskType: int = 0
    # 任务数值
    num: int = 0
    # 宝箱id
    boxId: int = 0
    # 消耗成就点
    cutPoints: int = 0
    # 宝箱奖励列表
    bItemList: dict = field(default_factory=dict)
    # 成就奖励id
    successId: int = 0
    # 所需消耗成就点数
    sCutPoints: int = 0
    # 成就奖励奖励列表
    sItemList: dict = field(default_factory=dict)

    def updateStatus(self, owner, taskId, data):
        taskStatusInfo = owner.taskStatusData.get(taskId)
        taskStatusInfo.addData('tData', data)
        current = taskStatusInfo.getData('tData')
        if current >= self.num:
            taskStatusInfo.setData('status', 1)
        return

    def isGetReward(self, owner, taskId):
        if owner.taskStatusData.get(taskId).getData('status', 0) != 1:
            return False
        return True

    def getReward(self, owner, taskId):
        owner.taskStatusData.get(taskId).setData('status', 2)
        return self.itemList


def onInit():
    for taskId, taskInfo in d_task.datas.items():
        taskTypeId = taskInfo.get('taskTypeId')
        itemId = list(taskInfo.get('itemId'))
        itemCount = list(taskInfo.get('itemCount'))
        itemList = dict(zip(taskInfo.get('itemId'), taskInfo.get('itemCount')))
        taskType = taskInfo.get('taskType')
        num = taskInfo.get('num')

        _taskDict.setdefault(taskTypeId, []).append(taskId)
        task = TaskConfig(
            taskId=taskId,
            taskTypeId=taskTypeId,
            itemId=itemId,
            itemCount=itemCount,
            itemList=itemList,
            taskType=taskType,
            num=num
        )
        _task_info[taskId] = task
    for boxId, boxInfo in d_task_box.datas.items():
        cutPoints = boxInfo.get('cutPoints')
        bItemList = dict(zip(boxInfo.get('bItemId'), boxInfo.get('bItemCount')))
        _box_info[boxId] = TaskConfig(
            boxId=boxId,
            cutPoints=cutPoints,
            bItemList=bItemList
        )

    for sId, sInfo in d_success_reward.datas.items():
        sCutPoints = sInfo.get('cutPoints')
        sItemList = dict(zip(sInfo.get('sItemId'), sInfo.get('sItemCount')))
        _success_reward_info[sId] = TaskConfig(
            successId=sId,
            sCutPoints=sCutPoints,
            sItemList=sItemList
        )


def getTaskInfo(taskId):
    return _task_info.get(taskId)


def getTaskDict(taskTypeId):
    return _taskDict.get(taskTypeId)


def getBoxInfo(boxId):
    return _box_info.get(boxId)


def getSuccessInfo(successId):
    return _success_reward_info.get(successId)


def getDayTask():
    dTaskList = random.sample(_taskDict.get(1), 4)
    aTaskList = _taskDict.get(2)
    return dTaskList, aTaskList


if __name__ == '__main__':
    onInit()
    getTaskDict(1)

    dTaskList, aTaskList = getDayTask()
    print(aTaskList)
