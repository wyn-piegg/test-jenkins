# -*- coding: utf-8 -*-
import datetime

from KBEDebug import *
import MESSAGE_CODE
from SUCCESS_REWARD import SuccessRewardStatus
from TASK_BOX import TaskBoxStatus
from TASK_REWARD import TaskReward
from TASK_STATUS import TaskStatus
import task


class TaskModule:
    def __init__(self):
        self.refreshDayTask()
        self.setSuccessStatus()
        self.setBoxStatus()

    def taskStatus(self, taskType, data):
        """
        修改任务状态
        @param taskType:
        @param data:
        @return:
        """
        task_type = self.taskType()
        taskList = task_type.get(taskType)
        if taskList is None:
            return

        for taskId in taskList:
            info = task.getTaskInfo(taskId)
            info.updateStatus(self, taskId, data)
        return

    def getReward(self, taskId):
        """
        获取奖励
        @param taskId:
        @return:
        """
        info = task.getTaskInfo(taskId)
        if info.isGetReward(self, taskId) is False:
            return self.onErrorMsg(MESSAGE_CODE.MC_TASK_REWARD_LESS)
        itemList = info.getReward(self, taskId)
        reward_result = []

        for itemId, count in itemList.items():
            reward_result.append(TaskReward().createFromDict(
                {'taskId': taskId, 'itemId': itemId, 'count': count}))

        self.client.onGetReward(reward_result)

    def setBoxStatus(self):
        """
        设置宝箱状态
        @return:
        """
        for boxId in task._box_info.keys():
            info = task.getBoxInfo(boxId)
            boxStatusInfo = self.boxStatus.get(boxId)
            if boxStatusInfo is None:
                boxStatusInfo = TaskBoxStatus().createFromDict({'boxId': boxId, 'status': 0})
                self.boxStatus[boxId] = boxStatusInfo
            boxStatusInfo = self.boxStatus.get(boxId)
            if self.activeValue >= info.cutPoints:
                boxStatusInfo.setData('status', 1)
        return

    def openBox(self, boxId):
        """
        开宝箱
        :return:
        """
        boxStatusInfo = self.boxStatus.get(boxId)
        info = task.getBoxInfo(boxId)
        if boxStatusInfo.getData('status') != 1:
            return self.onErrorMsg(MESSAGE_CODE.MC_BOX_REWARD_LESS)

        box_reward_result = []
        bItemList = info.bItemList

        for itemId, count in bItemList.items():
            box_reward_result.append(TaskReward().createFromDict(
                {'taskId': boxId, 'itemId': itemId, 'count': count}))

        boxStatusInfo.setData('status', 2)
        ERROR_MSG("-----------------------box_reward_result:%s" % box_reward_result)
        self.client.onOpenBox(box_reward_result)

    def setSuccessStatus(self):
        """
        设置成就任务状态
        @return:
        """
        for successId in task._success_reward_info.keys():
            info = task.getSuccessInfo(successId)
            successStatusInfo = self.successStatus.get(successId)
            if successStatusInfo is None:
                successStatusInfo = SuccessRewardStatus().createFromDict({'successId': successId, 'status': 0})
                self.successStatus[successId] = successStatusInfo
            if self.successPoints >= info.sCutPoints:
                successStatusInfo.setData('status', 1)
        return

    def getSuccessReward(self, successId):
        """
        领取成就奖励
        @param successId:
        @return:
        """
        successStatusInfo = self.successStatus.get(successId)
        info = task.getBoxInfo(successId)
        if successStatusInfo.getData('status') != 1:
            return self.onErrorMsg(MESSAGE_CODE.MC_SUCCESS_REWARD_LESS)

        success_reward_result = []
        sItemList = info.sItemList
        for itemId, count in sItemList.items():
            success_reward_result.append(TaskReward().createFromDict(
                {'taskId': successId, 'itemId': itemId, 'count': count}))

        successStatusInfo.setData('status', 2)

        self.client.onSuccessReward(success_reward_result)

    def refreshDayTask(self):
        """
        刷新每日任务
        @return:
        """

        now_time = int(datetime.datetime.now().strftime("%Y%m%d"))
        if now_time == self.lastLoginTime:
            return

        self.activeValue = 0

        dTaskList, aTaskList = task.getDayTask()

        if len(self.taskStatusData.keys()) == 0:
            for taskId in dTaskList + aTaskList:
                taskStatusInfo = TaskStatus().createFromDict({'taskId': taskId, 'tData': 0, 'status': 0})
                self.taskStatusData[taskId] = taskStatusInfo
            self.dayTaskList = dTaskList

        for taskId in self.dayTaskList:
            self.taskStatusData.pop(taskId, 0)

        for taskId in dTaskList:
            taskStatusInfo = TaskStatus().createFromDict({'taskId': taskId, 'tData': 0, 'status': 0})
            self.taskStatusData[taskId] = taskStatusInfo
        self.dayTaskList = dTaskList

    def taskType(self):
        """
        根据类型分类
        @return:
        """
        task_type = {}
        for taskId in self.taskStatusData.keys():
            info = task.getTaskInfo(taskId)
            task_type.setdefault(int(info.taskType), []).append(taskId)
        return task_type
