import base64
import json

import random

import operator
import re

import time
from datetime import datetime, timedelta

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Q
from django_redis import get_redis_connection
from django.http import JsonResponse
from backstage import models
from backstage.static.data.d_item import datas
from backstage.static.data import d_item, d_hero


def jump(request):
    return login(request)


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    account = request.POST.get('account')
    password = request.POST.get('password')
    conn = get_redis_connection('default')
    pwd = conn.get('admin')
    if pwd is None:
        return render(request, "login.html", {"error_msg": "登录失败,账号或密码错误"})

    pwd = str(pwd, encoding="utf-8")

    if pwd == password:
        request.session['token'] = account
        request.session.set_expiry(0)  # 0:表示关闭浏览器过期；None:表示永不过期。 默认两周后过期。
        return render(request, "home.html")

    return render(request, "login.html", {"error_msg": "登录失败,账号或密码错误"})


@csrf_exempt
def home_item_info(request):
    itemInfo = []
    for key, val in datas.items():
        itemInfo.append({"itemId": key, "name": val['name']})

    return JsonResponse(itemInfo, safe=False)


def pointUser(request):
    return render(request, "user_search.html")


# 用户信息
def user_search(request):
    return render(request, "user_search.html")


def userInfo(request):
    """查询用户信息"""
    uid = request.GET.get('userIdInfo')
    uName = request.GET.get('userNameInfo')
    arr = []
    if uid is None and uName is None:
        data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    if uid is not None:

        if models.TblAvatar.objects.filter(sm_uuid=uid).count() <= 0:
            data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )

        res = models.TblAvatar.objects.get(sm_uuid=uid)
    if uName is not None:
        if models.TblAvatar.objects.filter(sm_name=uName).count() <= 0:
            data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )

        res = models.TblAvatar.objects.get(sm_name=uName)

    guildInfo = models.TblGuildmanagerUid2GidValues.objects.filter(sm_uid=uid)
    guildName = ""
    if len(guildInfo) != 0:
        guildId = models.TblGuildmanagerUid2GidValues.objects.get(sm_uid=uid).sm_gid
        guildName = models.TblGuildmanagerGuildlistValues.objects.get(sm_gid=guildId).sm_guildname
    # diamond:钻石 silver:金币
    createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res.sm_createavatartime))
    lastTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res.sm_lastlogintime))

    arr.append({"uid": res.sm_uuid, "name": res.sm_name,
                "guildName": guildName,
                'lv': res.sm_level, "createTime": createTime,
                "lastTime": lastTime, "silver": res.sm_silver,
                "diamondNum": res.sm_diamond})
    data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


# 查询玩家英雄
def user_hero(request):
    return render(request, "user_hero.html")


def heroInfo(request):
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    startRow = (page - 1) * limit
    endRow = page * limit

    uid = request.GET.get('userIdInfo')
    uName = request.GET.get('userNameInfo')
    arr = []

    if uid is None and uName is None:
        data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    if uid is not None:
        if models.TblAvatar.objects.filter(sm_uuid=uid).count() <= 0:
            data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )
        pid = models.TblAvatar.objects.get(sm_uuid=uid).id

    if uName is not None:
        if models.TblAvatar.objects.filter(sm_name=uName).count() <= 0:
            data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )
        pid = models.TblAvatar.objects.get(sm_name=uName).id

    user_hero_info = models.TblAvatarHerolistValues.objects.filter(parentid=pid)

    for info in user_hero_info:
        hid = info.sm_hid
        res = models.TblAvatarHerolistValues.objects.filter(parentid=pid).get(sm_hid=hid)
        arr.append({"name": d_hero.datas.get(hid)['name'], "hid": res.sm_hid, "lv": res.sm_level})
    data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr[startRow:endRow]}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


# 查询玩家道具
def user_item(request):
    if request.method == "GET":
        return render(request, "user_item.html")
    info = {'code': True, 'info': '查无此人'}
    uid = request.POST.get("uid")

    name = request.POST.get("name")
    if uid is None and name is None:
        info['code'] = False
        return render(request, "user_item.html", {"info": info})

    if uid is None:
        user_info = models.TblAvatar.objects.filter(sm_name=name).first()
    else:
        user_info = models.TblAvatar.objects.filter(id=uid).first()

    if user_info is None:
        info['code'] = False
        return render(request, "user_item.html", {"info": info})

    item_info = models.TblAvatarUserbaginfoValues.objects.filter(parentid=user_info.id).all()
    if item_info is None:
        info['code'] = False
        return render(request, "user_hero.html", {"info": 'info'})
    itemList = {}
    for item in item_info:
        itemList[item.sm_itemId] = {}
        itemList[item.sm_itemId]['itemId'] = item.sm_itemId
        itemList[item.sm_itemId]['itemName'] = datas.get(item.sm_itemId, {"name": '未知道具'})['name']
        itemList[item.sm_itemId]['count'] = item.sm_count
    info['info'] = itemList
    return render(request, "user_item.html", {"info": info})


# 查询活跃
@csrf_exempt
def operate_active(request):
    if request.method == "GET":
        return render(request, "operate_active.html")


def day_active(request):
    datetimes = request.GET.get('time')
    if datetimes is None:
        return render(request, "operate_active.html")

    timeInfo = datetimes.split(' ~ ', 3)
    startTime = int(time.mktime(time.strptime(timeInfo[0], "%Y-%m-%d %H:%M:%S")))  # 年月日转时间戳
    endTime = int(time.mktime(time.strptime(timeInfo[1], "%Y-%m-%d %H:%M:%S")))

    user_info = models.TblAvatar.objects.all()
    len(user_info)

    h = (endTime - startTime) % 86400
    day = int((endTime - startTime) / 86400)

    y = []
    x = []

    if h != 0:
        day = day + 1
    if day > 1:
        while startTime <= endTime + (86400 - h):
            y.append(
                len(user_info) - models.TblAvatar.objects.filter(sm_lastlogintime__lte=startTime).all().count())
            x.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)))
            startTime += 86400

        arr = {'x': x, "y": y}

    if day <= 1:
        if (endTime - startTime) / 3600 < 1:
            s = (endTime - startTime) % 600
            while startTime <= endTime + (3600 - s):
                offLineUser = models.TblAvatar.objects.filter(sm_lastlogintime__gte=startTime,
                                                              sm_lastlogintime__lte=startTime + 600).all().count()
                onLineUser = len(user_info) - offLineUser - len(
                    models.TblAvatar.objects.filter(sm_lastlogintime__gt=startTime).all())

                y.append(offLineUser + onLineUser)
                x.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)).split(' ')[1])
                startTime += 600

            arr = {'x': x, "y": y}

        m = h % 3600
        while startTime <= endTime + (3600 - m):
            offLineUser = models.TblAvatar.objects.filter(sm_lastlogintime__gte=startTime,
                                                          sm_lastlogintime__lte=startTime + 3600).all().count()
            onLineUser = len(user_info) - offLineUser - len(
                models.TblAvatar.objects.filter(sm_lastlogintime__gt=startTime).all())

            y.append(offLineUser + onLineUser)

            x.append((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)).split(' ')[1] + "~" +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime + 3600)).split(' ')[1]))
            startTime += 3600

        arr = {'x': x, "y": y}

    # shijianchuo:600十分钟
    data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


# 查询新增
@csrf_exempt
def operate_new_user(request):
    if request.method == "GET":
        return render(request, "operate_new_user.html")


def new_user(request):
    datetimes = request.GET.get('time')
    if datetimes is None:
        return render(request, "operate_new_user.html")

    timeInfo = datetimes.split(' ~ ', 3)
    startTime = int(time.mktime(time.strptime(timeInfo[0], "%Y-%m-%d %H:%M:%S")))  # 年月日转时间戳
    endTime = int(time.mktime(time.strptime(timeInfo[1], "%Y-%m-%d %H:%M:%S")))

    user_info = models.TblAvatar.objects.filter(sm_createavatartime__gte=startTime,
                                                sm_createavatartime__lte=endTime).all()
    h = (endTime - startTime) % 86400
    day = int((endTime - startTime) / 86400)

    y = []
    x = []
    if h != 0:
        day = day + 1
    if day > 1:
        while startTime <= endTime + (86400 - h):
            y.append(
                len(user_info.filter(sm_createavatartime__gte=startTime,
                                     sm_createavatartime__lt=startTime + 86400).all()))
            x.append((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)).split(' ')[0] + "~" +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime + 86400)).split(' ')[0]))
            startTime += 86400

        arr = {'x': x, "y": y}

    if day <= 1:
        if (endTime - startTime) / 3600 < 1:
            s = (endTime - startTime) % 600
            while startTime <= endTime + (3600 - s):
                y.append(
                    len(user_info.filter(sm_createavatartime__gte=startTime,
                                         sm_createavatartime__lt=startTime + 600).all()))
                x.append((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)).split(' ')[1] + "~" +
                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime + 600)).split(' ')[1]))
                startTime += 600

            arr = {'x': x, "y": y}

        m = h % 3600
        while startTime <= endTime + (3600 - m):
            y.append(
                len(user_info.filter(sm_createavatartime__gte=startTime,
                                     sm_createavatartime__lt=startTime + 3600).all()))
            x.append((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)).split(' ')[1] + "~" +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime + 3600)).split(' ')[1]))
            startTime += 3600

        arr = {'x': x, "y": y}
    # shijianchuo:600十分钟
    data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


# 查询用户留存
def operate_user_keep(request):
    if request.method == "GET":
        return render(request, "operate_user_keep.html")

    datetimes = request.POST.get('datetimes')
    if datetimes is None:
        return render(request, "operate_user_keep.html")

    timeInfo = datetimes.split('-', 3)
    bTime = int(time.mktime(time.strptime(f"{timeInfo[0]}-{timeInfo[1]}-{timeInfo[2]}", "%Y-%m-%d %H:%M")))
    aTime = int(time.mktime(time.strptime(timeInfo[3], "%Y-%m-%d %H:%M")))

    info = {}
    while bTime <= aTime:
        info[bTime] = {}
        bTime += 86400

    for key, val in info.items():
        newCount = models.TblUsermanagerUserstatisticsValues.objects.filter(sm_time__gte=key,
                                                                            sm_time__lte=key + 86399). \
            aggregate(Sum('sm_increase'))
        info[key]["newCount"] = newCount
        timeInfo = time.strftime("%Y-%m-%d", time.localtime(key))
        info[key]['timeInfo'] = timeInfo
        val = [1, 2, 3, 4, 5, 6, 7, 15]
        for index in val:
            count = models.TblAvatarUserpublicinfoValues.objects.filter(sm_createtime__gte=key,
                                                                        sm_createtime__lte=key + 86399,
                                                                        sm_entergametime__gte=
                                                                        key + (86399 * index)).values(
                'parentid').count()
            info[key][index] = int((count / newCount['sm_increase__sum'] if newCount['sm_increase__sum'] else 0) / 100)
    # for userObject in user_info:
    #     x_axis.append(time.strftime("%Y-%m-%d %H:00:00", time.localtime(userObject.sm_time)))
    #     series_list.append(userObject.sm_increase)

    return render(request, "operate_user_keep.html", {"user_keep": info})


@csrf_exempt
def email_info(request):
    if request.method == "GET":

        total_row = models.KbeSiteEvent.objects.count()
        event_data = models.KbeSiteEvent.objects.filter(eventtype=1).order_by('-createtime')[0:10]

        page_data = []
        for data in event_data:
            tmp = {"id": data.id,
                   "eventtype": data.eventtype,
                   "is_confirm": data.is_confirm,
                   "createtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.createtime)),
                   "confirmtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.confirmtime)),
                   "sender": data.sender}
            event_body_dict = json.loads(data.eventbody)

            itemInfo = event_body_dict.get("itemInfo", None)
            tempInfo = {}
            if itemInfo is not None and len(itemInfo) > 0:
                for itemId, count in itemInfo.items():
                    item = d_item.datas.get(int(itemId), None)
                    if item is None:
                        key = 'err:' + itemId
                        tempInfo[key] = count
                    else:
                        tempInfo[item['name']] = count
                event_body_dict["itemInfo"] = tempInfo

            event_body_dict["sendTimes"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                         time.localtime(event_body_dict["sendTimes"]))
            event_body_dict["endTimes"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                        time.localtime(event_body_dict["endTimes"]))
            tmp.update(event_body_dict)
            page_data.append(tmp)

        return render(request, "email_info.html", {"total_row": total_row, "page_data": page_data, "curr_page": 1})

    curr_page = int(request.POST.get("curr_page"))  # 当前页
    request_page = int(request.POST.get("request_page"))  # 请求页
    data_top = (request_page - 1) * 10
    data_bottom = data_top + 10
    total_row = models.KbeSiteEvent.objects.count()
    event_data = models.KbeSiteEvent.objects.filter(eventtype=1).order_by('-createtime')[data_top:data_bottom]

    page_data = []
    for data in event_data:
        tmp = {"id": data.id,
               "eventtype": data.eventtype,
               "is_confirm": data.is_confirm,
               "createtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.createtime)),
               "confirmtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.confirmtime)),
               "sender": data.sender}
        event_body_dict = json.loads(data.eventbody)

        itemInfo = event_body_dict.get("itemInfo", None)
        tempInfo = {}
        if itemInfo is not None and len(itemInfo) > 0:
            for itemDict in itemInfo:
                for itemId, count in itemDict.items():
                    item = d_item.datas.get(int(itemId), None)
                    if item is None:
                        key = 'err:' + itemId
                        tempInfo[key] = count
                    else:
                        tempInfo[item['name']] = count
            event_body_dict["itemInfo"] = tempInfo

        event_body_dict["sendTimes"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event_body_dict["sendTimes"]))
        event_body_dict["endTimes"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event_body_dict["endTimes"]))
        tmp.update(event_body_dict)
        page_data.append(tmp)

    result = {"total_row": total_row, "page_data": page_data, "curr_page": request_page}
    return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def get_item_info(request):
    if request.method == "POST":
        pass


@csrf_exempt
def email_info_del(request):
    if request.method == "POST":
        del_id = request.POST.get('del_id')
        res = models.KbeSiteEvent.objects.filter(id=del_id).update(is_confirm=5)
        result = {"res": True, "del_id": del_id, "is_confirm": 5}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def email_send(request):
    if request.method == "GET":
        email_cookie = render(request, "email_send.html")
        email_cookie.set_cookie("item_info", 11)
        return render(request, "email_send.html")

    result = {"res": True, "message": '邮件发送成功!'}
    # 发送类型
    send_type = int(request.POST.get('email_send_type'))
    if send_type != 1 and send_type != 2:
        result['message'] = '邮件类型错误'
        return JsonResponse(result)

    # 发送范围
    send_range = request.POST.get('email_send_range')
    temp_List = [x for x in send_range.split(';') if x]
    send_list = []
    for uid in temp_List:
        send_list.append((uid))

    if send_type == 2:
        if len(send_list) <= 0:
            result['message'] = '邮件发送错误,无发送人'
            return JsonResponse(result)

    # 邮件标题
    send_title_temp = request.POST.get('email_send_title')
    send_title = send_title_temp.encode('utf-8')
    title_len = len(send_title)
    if 0 > title_len or title_len > 1000:
        result['message'] = '邮件发送标题错误'
        return JsonResponse(result)

    # 发送时间
    start_dates_temp = request.POST.get('email_send_starttimes')
    start_dates = time.strptime(start_dates_temp, '%Y-%m-%d %H:%M')
    exec_times = int(time.mktime(start_dates))
    if exec_times <= int(time.time()):
        result['message'] = '邮件发送时间错误'
        return JsonResponse(result)

    # 过期时间
    end_dates_temp = request.POST.get('email_send_endtimes')
    end_dates = time.strptime(end_dates_temp, '%Y-%m-%d %H:%M')
    end_times = int(time.mktime(end_dates))
    if end_times <= exec_times:
        result['message'] = '邮件过期时间错误'
        return JsonResponse(result)

    # 发送内容
    context_temp = request.POST.get('email_send_context')
    context = context_temp.encode('utf-8')
    context_len = len(context)
    if 0 > context_len or context_len > 10000000:
        result['message'] = '邮件发送内容错误'
        return JsonResponse(result)

    # 附件
    attached_info_temp = request.POST.get('email_send_attached')
    attached_info = json.loads(attached_info_temp)
    attached_info_dict = {}
    for item_info in attached_info:
        for item_id, item_count in item_info.items():
            if d_item.datas.get(int(item_id), None) is None or int(item_count) <= 0:
                return
            attached_info_dict[item_id] = item_count

    str(send_title, encoding="utf-8")
    email_body = {
        'title': str(send_title, encoding="utf-8"),
        'sendTimes': exec_times,
        'endTimes': end_times,
        'message': str(context, encoding="utf-8"),
        'itemInfo': attached_info_dict,
        'player': send_list,
        'source': send_type}

    eventType = 1  # 邮件
    eventBody = json.dumps(email_body)
    create_time = int(time.time())
    sender = "admin"

    models.KbeSiteEvent.objects.create(eventtype=eventType, eventbody=eventBody, is_confirm=0, exectime=exec_times,
                                       createtime=create_time, confirmtime=0, sender=sender)
    return JsonResponse(result)


@csrf_exempt
def message_send(request):
    if request.method == "GET":
        return render(request, "message_send.html")

    title_temp = request.POST.get('title', None)
    title = title_temp.encode('utf-8')
    message_temp = request.POST.get('message', None)
    message = message_temp.encode('utf-8')
    sendTime = request.POST.get('sendTime', None)
    messageType = request.POST.get('messageType', None)
    if title is None or message is None or sendTime is None or messageType is None:
        return JsonResponse({"res": True, "message": '添加失败'})

    send_dates = time.strptime(sendTime, '%Y-%m-%d %H:%M')
    send_times = int(time.mktime(send_dates))

    message_body = {
        'title': str(title, encoding="utf-8"),
        'message': str(message, encoding="utf-8"),
        'bulletinType': messageType}
    eventType = 2  # 公告
    eventBody = json.dumps(message_body)
    create_time = int(time.time())
    sender = "admin"

    models.KbeSiteEvent.objects.create(eventtype=eventType, eventbody=eventBody, is_confirm=0, exectime=send_times,
                                       createtime=create_time, confirmtime=0, sender=sender)

    result = {"res": True, "message": '添加成功!'}
    return JsonResponse(result)


@csrf_exempt
def message_info(request):
    if request.method == "GET":

        total_row = models.KbeSiteEvent.objects.count()
        event_data = models.KbeSiteEvent.objects.filter(eventtype=2).order_by('-createtime')[0:10]

        page_data = []
        for data in event_data:
            tmp = {"id": data.id,
                   "eventtype": data.eventtype,
                   "is_confirm": data.is_confirm,
                   "createtime": data.createtime,
                   "confirmtime": data.confirmtime,
                   "exectime": data.exectime,
                   "sender": data.sender}
            event_body_dict = json.loads(data.eventbody)
            tmp.update(event_body_dict)
            tmp['exectime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tmp['exectime']))
            page_data.append(tmp)
        return render(request, "message_info.html", {"total_row": total_row, "page_data": page_data, "curr_page": 1})

    curr_page = int(request.POST.get("curr_page"))  # 当前页
    request_page = int(request.POST.get("request_page"))  # 请求页
    data_top = (request_page - 1) * 10
    data_bottom = data_top + 10
    total_row = models.KbeSiteEvent.objects.count()
    event_data = models.KbeSiteEvent.objects.filter(eventtype=2).order_by('-createtime')[data_top:data_bottom]

    page_data = []
    for data in event_data:
        tmp = {"id": data.id,
               "eventtype": data.eventtype,
               "is_confirm": data.is_confirm,
               "createtime": data.createtime,
               "confirmtime": data.confirmtime,
               "exectime": data.exectime,
               "sender": data.sender}
        event_body_dict = json.loads(data.eventbody)

        tmp.update(event_body_dict)
        tmp['exectime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tmp['exectime']))
        page_data.append(tmp)

    result = {"total_row": total_row, "page_data": page_data, "curr_page": request_page}
    return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def message_info_del(request):
    if request.method == "POST":
        del_id = request.POST.get('del_id')
        res = models.KbeSiteEvent.objects.filter(id=del_id).update(is_confirm=5)
        result = {"res": True, "del_id": del_id, "is_confirm": 5}
        return HttpResponse(json.dumps(result), content_type="application/json")


def test(request):
    return render(request, "login1.html")


@csrf_exempt
def activationInfo(request):
    """激活码信息"""

    activationList = models.KbeActivation.objects.all()

    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    startRow = (page - 1) * limit
    endRow = page * limit

    c = []

    for activation_info in activationList:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        end_time = (str(activation_info.end_time)[0:19])

        nTime = datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
        eTime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if activation_info.is_del == 0:
            continue
        if eTime.timestamp() * 1000 - nTime.timestamp() * 1000 <= 0:
            activation_info.is_del = 0
            activation_info.code_status = 0
            activation_info.save()
            continue

        start_time = (str(activation_info.start_time)[0:19])

        activation = {"id": activation_info.id, "activationCode": activation_info.activation_code,
                      'itemId': activation_info.item_id,
                      "itemName": activation_info.item_name, "itemCount": activation_info.item_count,
                      "code_status": activation_info.code_status, "startTime": start_time,
                      "endTime": end_time, "useNum": activation_info.use_num}
        c.append(activation)
    count = len(c)
    arr = c[startRow:endRow]

    # arr.sort(key=operator.itemgetter('code_status'), reverse=True)

    data = {'code': 0, 'msg': 'OK', 'count': count, 'data': arr}

    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def addActivationCode(request):
    """生成激活码"""

    last_code = ''.join(random.sample('ABCDEFGHIJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz123456789', 8)).replace(" ",
                                                                                                               "")
    l = list(str(last_code))
    l.sort()
    code = ''.join(l)
    activation_code = str(base64.b64encode(code.encode("utf-8")), "utf-8")

    item_id = request.POST.get("itemId")
    itemName = request.POST.get("itemName")
    itemCount = request.POST.get("itemCount")
    timeScope = request.POST.get("time")
    timeList = timeScope.split(' ~ ', 3)
    if item_id is None or itemName is None or itemCount is None or timeScope is None or timeList is None:
        return JsonResponse({"res": True, "message": '添加失败'})

    code = request.POST.get("code")

    if code is not None:
        if models.KbeActivation.objects.filter(activation_code=code).count() > 0:
            data = {"res": False, 'code': 0, 'msg': '已存在激活码', 'count': 1}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )
        activation_code = code

    models.KbeActivation.objects.create(activation_code=activation_code, item_id=item_id,
                                        item_name=itemName,
                                        item_count=itemCount, code_status=1, start_time=timeList[0],
                                        end_time=timeList[1], is_del=1, use_num=0)

    data = {"res": True, 'code': 0, 'msg': '添加成功', 'count': 1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def delActivationCode(request):
    """删除还未发出的激活码"""
    aid = request.GET.get('id')
    info = models.KbeActivation.objects.filter(id=aid)
    info.update(is_del=0)
    info.update(code_status=3)
    return redirect("/operate/createActivationCode")


def createActivationCode(request):
    """生成激活码页面"""

    return render(request, "create_activation_code.html")


def activationCode(request):
    """激活码页面"""
    return render(request, "activation_code.html")


def activationCodeInfo(request):
    """激活码页面"""

    activationList = models.KbeActivation.objects.all()

    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    startRow = (page - 1) * limit
    endRow = page * limit

    c = []

    for activation_info in activationList:
        end_time = (str(activation_info.end_time)[0:19])

        start_time = (str(activation_info.start_time)[0:19])

        activation = {"id": activation_info.id, "activationCode": activation_info.activation_code,
                      'itemId': activation_info.item_id,
                      "itemName": activation_info.item_name, "itemCount": activation_info.item_count,
                      "code_status": activation_info.code_status, "startTime": start_time,
                      "endTime": end_time, "useNum": activation_info.use_num}
        c.append(activation)
    count = len(c)
    arr = c[startRow:endRow]

    # arr.sort(key=operator.itemgetter('code_status'), reverse=True)

    data = {'code': 0, 'msg': 'OK', 'count': count, 'data': arr}

    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def editCodeStatus(request):
    """修改激活信息"""
    aid = request.GET.get("id")
    status = str(request.GET.get("status"))

    if status == "false":
        models.KbeActivation.objects.filter(id=aid).update(code_status=0)
    if status == "true":
        models.KbeActivation.objects.filter(id=aid).update(code_status=1)

    return redirect("/operate/createActivationCode")


def selActivationCode(request):
    """查询激活码信息"""
    info = request.GET.get('codeInfo')

    arr = []
    # q.children.append(('item_name__contains', info))
    # res = models.KbeActivation.objects.filter(q)

    res = models.KbeActivation.objects.filter(activation_code=info)

    if res.count() <= 0:
        data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    for r in res:
        end_time = (str(r.end_time)[0:19])

        start_time = (str(r.start_time)[0:19])
        arr.append({"id": r.id, "activationCode": r.activation_code,
                    'itemId': r.item_id,
                    "itemName": r.item_name, "itemCount": r.item_count,
                    "code_status": r.code_status, "startTime": start_time, "endTime": end_time, "useNum": r.use_num})

    data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def exchange_cdk(request):
    """ 激活码兑换 """
    try:
        uuid = request.GET.get('uuid')
        dbid = request.GET.get('dbid')
        name = request.GET.get('name')
        cdk = request.GET.get('cdk')

        cdkInfo = models.KbeActivation.objects.filter(activation_code=cdk).first()
        if cdkInfo is None:
            return HttpResponse(json.dumps({"code": 10001, "subCode": 18005, "msg": "cdk无效"}))

        if cdkInfo.is_del == 0 or cdkInfo.code_status == 0:
            return HttpResponse(json.dumps({"code": 10001, "subCode": 18002, "msg": "cdk无效"}))

        res = models.KbeCdkRecode.objects.filter(dbid=dbid, cdk=cdk)
        if res.count() != 0:
            return HttpResponse(json.dumps({"code": 10001, "subCode": 18001, "msg": "已经领取过"}, ensure_ascii=False), )

        if not cdkInfo.start_time.timestamp() < datetime.now().timestamp() <= cdkInfo.end_time.timestamp():
            return HttpResponse(json.dumps({"code": 10001, "subCode": 18003, "msg": "cdk已过期"}))

        item_id = [int(x) for x in re.split(",+|=+", cdkInfo.item_id) if x]
        item_count = [int(x) for x in re.split(",+|=+", cdkInfo.item_count) if x]
        item_info = dict(zip(item_id, item_count))
        cdkInfo.use_num += 1
        cdkInfo.save()

        exchange_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        models.KbeCdkRecode.objects.create(dbid=dbid, name=name, cdk=cdkInfo.activation_code,
                                           create_date=exchange_date)

    except Exception as e:
        HttpResponse(json.dumps({"code": 10002, "subCode": 18004, "msg": "cdk处理失败"}))
        raise e

    return HttpResponse(
        json.dumps(
            {"code": 10000, "subCode": 18000, "msg": "", "dbid": dbid, "uuid": uuid, "cdk": cdkInfo.activation_code,
             "itemInfo": item_info},
            ensure_ascii=False), )


def codeRecord(request):
    """激活码领取记录"""
    if request.method == "GET":
        return render(request, "codeRecord.html")

    uid = request.POST.get("uid")
    code = request.POST.get("code")

    if uid is not None:
        res = models.TblAvatar.objects.filter(sm_uuid=uid)
        if res.count() <= 0:
            return HttpResponse(json.dumps({'code': 0, 'count': 1, 'data': 0, "msg": "没有此用户"}, ensure_ascii=False), )
        uInfo = models.TblAvatar.objects.get(sm_uuid=uid)

        codeRes = models.KbeCdkRecode.objects.filter(dbid=uInfo.id)

        arr = []

        if codeRes.count() <= 0:
            arr.append({"name": res.sm_name, "uid": res.sm_uuid, "code": "", "createTime": ""})
            data = {'code': 0, 'msg': 'OK', 'count': 1, 'data': arr}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )

        for c in codeRes:
            arr.append({"name": c.name, "uid": uid, "code": c.cdk, "createTime": str(c.create_date)})
        data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    if code is not None:
        codeRes = models.KbeCdkRecode.objects.filter(cdk=code)
        arr = []
        if codeRes.count() <= 0:
            return HttpResponse(
                json.dumps({'code': 0, 'count': 1, 'data': 0, "msg": "此激活码没有领取信息"}, ensure_ascii=False), )

        for c in codeRes:
            uid = models.TblAvatar.objects.get(id=c.dbid).sm_uuid

            arr.append({"name": c.name, "uid": uid, "code": c.cdk, "createTime": str(c.create_date)})
        data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )


def codeRecordInfo(request):
    cdkRecordInfo = models.KbeCdkRecode.objects.all()
    arr = []
    for c in cdkRecordInfo:
        uid = models.TblAvatar.objects.get(id=c.dbid).sm_uuid
        arr.append({"name": c.name, "uid": uid, "code": c.cdk, "createTime": str(c.create_date)})
    data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )
