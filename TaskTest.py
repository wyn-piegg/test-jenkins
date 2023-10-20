# -*- coding: utf-8 -*-
import datetime

import TASK_STATUS
from KBEDebug import *
import MESSAGE_CODE
from SUCCESS_REWARD import SuccessRewardStatus
from TASK_BOX import TaskBoxStatus
from TASK_REWARD import TaskReward
from TASK_STATUS import TaskStatus
import task
import TASK_TEST


class taskDataHandle:
    def __init__(self, taskStatusData):
        self.taskData = taskStatusData
        self.taskListData = {}
        self.dayTask = []
        self.init()

    def init(self):
        for taskId, taskData in self.taskData.items():
            info = task.getTaskInfo(taskId)
            self.taskListData.setdefault(info.taskListId, {}).setdefault(taskId, taskData)
            if info.taskListId == 1:
                self.dayTask.append(taskId)

    def removeDayTask(self, taskId):
        self.taskData.pop(taskId)

    def clearDayTask(self):
        for taskId in self.dayTask:
            self.taskData.pop(taskId)

    def updataTask(self, taskId, val, state):
        taskObj = self.taskData.get(taskId)
        taskObj.setData("tData", val)
        taskObj.setData("state", val)

    def getTask(self, taskId):
        taskObj = self.taskData.get(taskId)
        task = Task(taskObj)

        return task

    taskObj = getTask(111)

    taskObj.data = 50
    taskObj.checkTaskStatus()
    taskObj.status = 1


class Task:
    def __init__(self, taskInfo):
        self.taskInfo = taskInfo

    @property
    def data(self):
        return self.taskInfo.getData("tData")

    @data.setter
    def data(self, val):
        self.taskInfo.setData("tData", val)

    @property
    def status(self):
        return self.taskInfo.getData("status")


class TaskModule:
    def __init__(self):
        self.taskListData = taskDataHandle(self.taskStatusData)
        self.initTaskData()
        self.refreshDayTask()
        self.setSuccessStatus()
        self.setBoxStatus()

        self.taskListData.clearDayTask()
        self.taskListData.taskData

    def initTaskData(self):
        for taskId, taskData in self.taskStatusData.items():
            info = task.getTaskInfo(taskId)
            self.taskListData.setdefault(info.taskListId, {}).setdefault(taskId, taskData)

    def test(self):
        data = {}
        data[123] = TASK_STATUS.TaskStatus().createFromDict({'taskId': 123, 'tData': 1, 'status': 1})
        data[456] = TASK_STATUS.TaskStatus().createFromDict({'taskId': 456, 'tData': 11, 'status': 0})
        self.taskTest[1] = TASK_TEST.TaskTest().createFromDict({'taskType': 1, 'task_list': data})
        self.taskTest[2] = TASK_TEST.TaskTest().createFromDict({'taskType': 2, 'task_list': data})

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
        ERROR_MSG("-------------------task._box_info.keys():%s" % task._box_info.keys())
        for boxId in task._box_info.keys():

            info = task.getBoxInfo(boxId)
            boxStatusInfo = self.boxStatus.get(boxId)
            if boxStatusInfo is None:
                boxStatusInfo = TaskBoxStatus().createFromDict({'boxId': boxId, 'status': 0})
                self.boxStatus[boxId] = boxStatusInfo
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

        taskList = self.taskListData.get(1)
        taskListData = self.taskListData.get(2)

        if len(taskList) > 0:
            for taskId in taskList:
                self.taskStatusData.pop(taskId, 0)

        for taskId in dTaskList:
            taskStatusInfo = TaskStatus().createFromDict({'taskId': taskId, 'tData': 0, 'status': 0})
            self.taskStatusData[taskId] = taskStatusInfo
        self.taskListData[1] = dTaskList

        if len(taskListData) == 0:
            for taskId in aTaskList:
                taskStatusInfo = TaskStatus().createFromDict({'taskId': taskId, 'tData': 0, 'status': 0})
                self.taskStatusData[taskId] = taskStatusInfo
            self.taskListData[2] = aTaskList

    def taskType(self):
        """
        根据类型分类
        @return:
        """
        task_type = {}
        ERROR_MSG(
            "--------------------taskType----------------------self.taskListData.get(1):%s self.taskListData.get(2):%s" % (
                self.taskListData.get(1), self.taskListData.get(2)))
        for taskId in self.taskListData.get(1) + self.taskListData.get(2):
            info = task.getTaskInfo(taskId)
            task_type.setdefault(int(info.taskType), []).append(taskId)
        ERROR_MSG("------------------------------taskType-------------------------task_type:%s" % task_type)
        return task_type


{111006: [111006, 0, 0], 111010: [111010, 0, 0], 111009: [111009, 0, 0], 111016: [111016, 0, 0], 211007: [211007, 0, 0],
 211008: [211008, 0, 0], 211009: [211009, 0, 0], 211010: [211010, 0, 0], 211011: [211011, 0, 0], 211012: [211012, 0, 0],
 211013: [211013, 0, 0], 211014: [211014, 0, 0], 211015: [211015, 0, 0], 211016: [211016, 0, 0], 211017: [211017, 0, 0],
 211018: [211018, 0, 0], 211019: [211019, 0, 0], 211020: [211020, 0, 0], 211021: [211021, 0, 0], 111015: [111015, 0, 0],
 111013: [111013, 0, 0], 111012: [111012, 0, 0], 111008: [111008, 0, 0], 111007: [111007, 0, 0], 111014: [111014, 0, 0],
 111011: [111011, 0, 0]}
