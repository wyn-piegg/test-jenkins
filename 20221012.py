# -*- coding: utf-8 -*-
import time

import KBEngine

import Functor
from KBEDebug import *


class RankListManager:
    def __init__(self):
        self.fixed = 1640966400
        self.rankTypeMap = {1: "rankList", 2: "achievement"}

    def getScore(self, score):

        # return score + +
        return int(10000000 - (time.time() - self.fixed)) * 100000 + score

        # return str(score)  # 带时间戳的分数去掉后10位就是实际分数

    def rGetRankId(self, rankType):
        """
        找到第101名的uid
        @param rankType:
        @return:
        """
        rankKey = self.rankTypeMap.get(rankType)
        sql = f"ZREVRANGE {rankKey}:{rankType} 100 101"
        KBEngine.executeRawDatabaseCommand(sql, self.getRankCallback, -1, "redis")

    def rGetRankHundredPoints(self, rankType):
        """
        找到第101名的分数
        @param rankType:
        @return:
        """
        rankKey = self.rankTypeMap.get(rankType)
        sql = f"ZSCORE {rankKey}:{rankType} {self.rGetRankId(rankType)}"
        KBEngine.executeRawDatabaseCommand(sql, self.getRankCallback, -1, "redis")

    def delLastHundred(self, rankType):
        """
        删除后一百名的信息

        @param rankType:
        @return:
        """
        rankKey = self.rankTypeMap.get(rankType)
        sql = f"ZREMRANGEBYSCORE {rankKey}:{rankType} {0} {self.rGetRankId}"
        KBEngine.executeRawDatabaseCommand(sql, self.addCallback, -1, "redis")

    # def rGetRankListNum(self, rankType):
    #     """
    #     查看目前排行榜有多少人
    #     @param rankType:
    #     @return:
    #     """
    #     sql = f"ZCARD RankList:{rankType}"
    #     KBEngine.executeRawDatabaseCommand(sql, Functor.Functor(self.getCallback), -1, "redis")

    def rAddRankList(self, rankType, points, uid):
        """
        加入排行榜
        @param rankType:
        @param points:
        @param uid:
        @return:
        """

        rankKey = self.rankTypeMap.get(rankType)
        score = self.getScore(points)
        sql = f"ZADD {rankKey}:{rankType} {score} {uid}"
        KBEngine.executeRawDatabaseCommand(sql, Functor.Functor(self.addCallback, uid), -1, "redis")

    # def rDelRankList(self, rankType, uuid):
    #     """
    #     删除第100名在排行榜中的信息
    #     @param rankType:
    #     @param uuid:
    #     @return:
    #     """
    #     sql = f"ZREM RankList:{rankType} {uuid}"
    #     KBEngine.executeRawDatabaseCommand(sql, Functor.Functor(self.addCallback), -1, "redis")

    def rGetRankHundredInfo(self, owner, rankType):
        """
        获取前100名信息
        @param rankType:
        @return:
        """
        sql = f"ZREVRANGE RankList:{rankType} 0 100"
        KBEngine.executeRawDatabaseCommand(sql, (self.getRankCallback, owner, rankType), -1, "redis")

    def userReportedData(self, uid, rankType, data):
        """
        用户上报数据
        @param rankType:
        @param data:
        @return:
        """
        self.rAddRankList(uid, rankType, data)

    # --------------------------------------------------------------------------------------------
    #                                          callBack
    # --------------------------------------------------------------------------------------------

    def getRankCallback(self, owner, rankType, result, rows, insertid, error):
        DEBUG_MSG("result: %s, rows: %s, insertid: %s, error: %s" % (str(result), str(rows), str(insertid), str(error)))
        uidList = []
        for i in result[0]:
            uidList.append(str(i, encoding="utf8"))
        DEBUG_MSG("---- result:%s ----" % uidList)

        owner.getRankResult(rankType, uidList)

    def addCallback(self, uid, result, rows, insertid, error):
        result = str(result[0][0], encoding="utf8")
        if result == "OK":
            return

        ERROR_MSG('addCallback:FId-Error[%i],result[%s]' % (uid, result))
