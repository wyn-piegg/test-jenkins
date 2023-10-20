# -*- coding: utf-8 -*-


def wordOnlines(newsType, users):
    """
    统计世界在线人数
    @param newsType:
    @param users:
    @return:
    """
    online = []
    if newsType != GlobalConst.CHAT_TYPE_WORD:
        return
    for i in range(len(users)):
        online.append(users[i][0])
    return online


def laborUnionOlines(newsType, users, laborUnionId):
    """
    统计工会在线人数
    @param newsType:
    @param users:
    @param laborUnionId:
    @return:
    """
    online = []
    if newsType != GlobalConst.CHAT_TYPE_LABOR_UNION:
        return
    for i in range(len(users)):
        i.laborUnionId = laborUnionId
        online.append(users[i][0])
    return online
