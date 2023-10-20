import base64
import json
import os

from django.forms import forms
from django.shortcuts import render
import random
import urllib.request
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

import game.scheduler
from cms import models
from common_static.data import d_item, d_hero
import game.models
from django.conf import settings

# Create your views here.
from game.views import email_send_to_server

from cms.tencentcos import cos_client


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
def email_info(request):
    if request.method == "GET":
        return render(request, "email_info.html")


def emailInfo(request):
    """"""
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    startRow = (page - 1) * limit
    endRow = page * limit

    count = models.KbeMail.objects.count()
    event_data = models.KbeMail.objects.filter().order_by('-id')[startRow:endRow]

    page_data = []
    for data in event_data:
        if data.sendtype == 1:
            sendType = "全服"
        elif data.sendtype == 2:
            sendType = "个人"

        elif data.sendtype == 3:
            sendType = "等级"
        else:
            sendType = "渠道"

        tmp = {
            "id": data.id,
            "title": data.title,
            "message": data.message,
            "itemdict": eval(data.itemdict),
            "userlist": data.userlist,
            "sendtype": sendType,
            "sendtime": data.sendtime,
            "state": data.state,
            'sendTimeType': data.sendtimetype,
        }
        page_data.append(tmp)

    data = {'code': 0, 'msg': 'OK', 'count': count, 'data': page_data}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


@csrf_exempt
def email_info_del(request):
    if request.method == "POST":
        del_id = request.POST.get('del_id')
        result = {"res": True, "del_id": del_id, "state": 2, 'message': '取消成功'}
        try:
            info = game.scheduler.jobs_info()
            if del_id not in [i.id for i in info]:
                result['res'] = False
                result['message'] = '无此任务'
                return HttpResponse(json.dumps(result), content_type="application/json")
            game.scheduler.remove_job_id(del_id)
        except:
            result['res'] = False
            result['message'] = '取消失败'
            return HttpResponse(json.dumps(result), content_type="application/json")

        res = models.KbeMail.objects.filter(id=del_id).update(state=settings.EMAIL_SEND_CANCEL_SUCCESS)

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

    time_type = int(request.POST.get('email_send_time_type', 0))
    if time_type != 1 and time_type != 2:
        result['message'] = '邮件时间类型错误'
        return JsonResponse(result)

    # 发送范围
    send_range = request.POST.get('email_send_range')
    if send_type == 2:
        temp_List = [x for x in send_range.split(',') if x]
        send_list = []
        for uid in temp_List:
            send_list.append((uid))
        if len(send_list) <= 0:
            result['message'] = '邮件发送错误,无发送人'
            return JsonResponse(result)

    # TODO:邮件等级发送处理
    if send_type == 3:
        pass
    # TODO:邮件渠道发送处理
    if send_type == 4:
        pass

    # 邮件标题
    send_title_temp = request.POST.get('email_send_title')
    send_title = send_title_temp.encode('utf-8')
    title_len = len(send_title)
    if 0 > title_len or title_len > 1000:
        result['message'] = '邮件发送标题错误'
        return JsonResponse(result)

    # 发送时间
    sendTime = int(time.time())
    runDate = None
    if time_type == 1:
        start_dates_temp = request.POST.get('email_send_starttimes')
        start_dates = time.strptime(start_dates_temp, '%Y-%m-%d %H:%M')
        runDate = datetime.strptime(start_dates_temp, '%Y-%m-%d %H:%M')
        sendTime = int(time.mktime(start_dates))
        if sendTime <= int(time.time()):
            result['message'] = '邮件发送时间错误'
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

    # 数据库插记录
    createObj = models.KbeMail.objects.create(
        title=send_title_temp,
        message=context_temp,
        userlist=send_list,
        itemdict=attached_info_dict,
        sendtype=send_type,
        sendtime=sendTime,
        state=settings.EMAIL_SEND_WAIT,
        sendtimetype=time_type
    )

    email_body = {
        'sendId': createObj.id,
        'title': send_title_temp,
        'message': context_temp,
        'itemDict': attached_info_dict,
        'userList': send_list,
        'sendType': send_type
    }

    if time_type == 1:
        if runDate is None:
            result['message'] = '邮件定时发送失败'
            return JsonResponse(result)
        try:
            game.scheduler.add_job_date(email_send_to_server, runDate, [email_body], str(createObj.id))
        except:
            models.KbeMail.objects.filter(id=createObj.id).update(state=settings.EMAIL_SEND_FAIL)
            result['message'] = '邮件定时发送失败'
            return JsonResponse(result)
        return JsonResponse(result)

    val = email_send_to_server(email_body)
    return JsonResponse(val)


def searchEmail(request):
    """查询邮件"""
    emailType = int(request.GET.get("emailType"))
    searchInfo = request.GET.get("searchInfo")
    sendType = "全服"

    arr = []
    emailInfos = models.KbeMail.objects.filter(sendtype=emailType)
    if emailInfos.count() <= 0:
        data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': {}}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    if len(searchInfo) <= 0:
        for info in emailInfos:
            arr.append({"id": info.id,
                        "title": info.title,
                        "message": info.message,
                        "itemdict": eval(info.itemdict),
                        "userlist": info.userlist,
                        "sendtype": sendType,
                        "sendtime": info.sendtime,
                        "state": info.state,
                        'sendTimeType': info.sendtimetype})

        data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    if emailType == 2:
        sendType = "单人"
        for info in emailInfos:
            if str(searchInfo) in info.userlist:
                arr.append({"id": info.id,
                            "title": info.title,
                            "message": info.message,
                            "itemdict": eval(info.itemdict),
                            "userlist": info.userlist,
                            "sendtype": sendType,
                            "sendtime": info.sendtime,
                            "state": info.state,
                            'sendTimeType': info.sendtimetype})
        if len(arr) <= 0:
            data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': {}}
            return HttpResponse(json.dumps(data, ensure_ascii=False), )

        data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )


@csrf_exempt
def message_send(request):
    if request.method == "GET":
        return render(request, "message_send.html")

    title = request.POST.get('title', None)
    message = request.POST.get('message', None)
    sendTime = request.POST.get('sendTime', None)
    messageType = request.POST.get('messageType', None)
    if title is None or message is None or sendTime is None:
        return JsonResponse({"res": True, "message": '添加失败'})

    create_time = int(time.time())
    source = 0
    data = {
        "messageType": messageType,
        "title": title,
        "message": message,
        "sendTime": create_time,
        "source": source,
    }

    val = requestGame(data, settings.GAME_BULLETIN_TYPE)
    # if val['res'] is True:
    #     # 数据库插记录
    #     models.KbeBulletin.objects.create(title=title, message=message, source=source, sendtime=create_time,
    #                                       bulletintype=messageType, state=1)

    return JsonResponse(val)


@csrf_exempt
def message_info(request):
    if request.method == "GET":
        return render(request, "message_info.html")


def messageInfo(request):
    """"""
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page is None or limit is None:
        return HttpResponse(json.dumps({'code': 0, 'msg': 'error', 'count': 0, 'data': []}, ensure_ascii=False), )

    page = int(page)
    limit = int(limit)
    startRow = (page - 1) * limit
    endRow = page * limit

    total_row = models.KbeBulletin.objects.count()
    if total_row < startRow:
        return HttpResponse(json.dumps({'code': 0, 'msg': 'OK', 'count': 0, 'data': []}, ensure_ascii=False), )

    event_data = models.KbeBulletin.objects.filter().order_by('-id')[startRow:endRow]

    page_data = []
    for data in event_data:
        tmp = {"id": data.id,
               "title": data.title,
               "message": data.message,
               "sendTime": data.sendtime,
               "source": data.source,
               "bulletinType": data.bulletintype,
               "state": data.state}
        page_data.append(tmp)

    data = {'code': 0, 'msg': 'OK', 'count': total_row, 'data': page_data}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


@csrf_exempt
def message_info_del(request):
    if request.method == "POST":
        del_id = request.POST.get('del_id')
        res = models.KbeBulletin.objects.filter(id=del_id).update(state=2)
        result = {"res": True, "del_id": del_id, "state": 2}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def activationInfo(request):
    """激活码信息"""

    activationList = models.KbeActivation.objects.order_by('-id')

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

        if activation_info.is_del == 0 or activation_info.code_status == 3:
            continue
        if eTime.timestamp() * 1000 - nTime.timestamp() * 1000 <= 0:
            activation_info.is_del = 0
            activation_info.code_status = 3
            activation_info.save()
            continue

        isIndividual = "全服"
        canUseNum = "不限次数"
        if activation_info.code_use_obj != "-1":
            isIndividual = activation_info.code_use_obj

        if activation_info.can_use_num != -1:
            canUseNum = activation_info.can_use_num

        start_time = (str(activation_info.start_time)[0:19])

        activation = {"id": activation_info.id, "cdk_title": activation_info.cdk_title,
                      "activationCode": activation_info.activation_code,
                      'itemId': activation_info.item_id,
                      "itemName": activation_info.item_name, "itemCount": activation_info.item_count,
                      "code_status": activation_info.code_status, "startTime": start_time,
                      "endTime": end_time, "useNum": activation_info.use_num,
                      "isIndividual": isIndividual, "canUseNum": canUseNum}
        c.append(activation)
    count = len(c)
    arr = c[startRow:endRow]

    data = {'code': 0, 'msg': 'OK', 'count': count, 'data': arr}

    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def addActivationCode(request):
    """生成激活码"""

    codeCount = request.POST.get("codeCount")
    if codeCount is None:
        codeCount = 0

    codeList = []
    for i in range(0, int(codeCount)):
        last_code = ''.join(random.sample('ABCDEFGHJKIMNPQRSTUVWXYZabcdefghijkmnpqrstuOovwxyz12345670', 11)).replace(
            " ",
            "")
        l = list(str(last_code))
        l.sort()
        code = ''.join(l)

        activation_code = str(base64.b64encode(code.encode("utf-8")), "utf-8")
        a1 = activation_code.replace("o", "d")
        a2 = a1.replace("O", "f")
        a3 = a2.replace("0", "e")
        a4 = a3.replace("l", "w")
        a5 = a4.replace("=", "w")
        activation_code = a5.replace("I", "a")
        codeList.append(activation_code[0:10])

    item_id = request.POST.get("itemId")
    itemName = request.POST.get("itemName")
    itemCount = request.POST.get("itemCount")
    timeScope = request.POST.get("time")
    title = request.POST.get("title")
    useCount = request.POST.get("useCount")
    codeUseObj = request.POST.get("codeUseObj")

    timeList = timeScope.split(' ~ ', 3)
    result = {"res": True, "message": '激活码添加成功!'}

    if item_id is None or itemName is None or itemCount is None or timeScope is None or timeList is None:
        result['message'] = '添加失败'
        return JsonResponse(result)

    code = request.POST.get("code")

    if code is not None:
        if models.KbeActivation.objects.filter(activation_code=code).count() > 0:
            result['message'] = '已存在激活码'
            return JsonResponse(result)
        codeList.append(code)

    if len(useCount) <= 0:
        useCount = -1
    if len(codeUseObj) <= 0:
        codeUseObj = -1

    for i in range(0, len(codeList)):
        models.KbeActivation.objects.create(activation_code=codeList[i], item_id=item_id,
                                            item_name=itemName,
                                            item_count=itemCount, code_status=1, start_time=timeList[0],
                                            end_time=timeList[1], is_del=1, use_num=0, cdk_title=title,
                                            can_use_num=useCount, code_use_obj=codeUseObj)

    data = {"res": True, 'code': 0, 'message': '添加成功', 'count': 1}
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

    activationList = models.KbeActivation.objects.order_by('-id')

    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    startRow = (page - 1) * limit
    endRow = page * limit

    c = []

    for activation_info in activationList:
        useCount = "不限次数"
        cdkUseObj = "全服玩家"
        end_time = (str(activation_info.end_time)[0:19])

        start_time = (str(activation_info.start_time)[0:19])

        if activation_info.can_use_num != -1:
            useCount = activation_info.can_use_num

        if activation_info.code_use_obj != "-1":
            cdkUseObj = activation_info.code_use_obj
        activation = {"id": activation_info.id, "activationCode": activation_info.activation_code,
                      'itemId': activation_info.item_id,
                      "itemName": activation_info.item_name, "itemCount": activation_info.item_count,
                      "code_status": activation_info.code_status, "startTime": start_time,
                      "endTime": end_time, "useCount": useCount, "useNum": activation_info.use_num,
                      "cdk_title": activation_info.cdk_title, "cdkUseObj": cdkUseObj}
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
            return HttpResponse(json.dumps({"code": 18006, "subCode": 18005, "msg": "cdk无效"}))

        if cdkInfo.is_del == 0 or cdkInfo.code_status == 0:
            return HttpResponse(json.dumps({"code": 18006, "subCode": 18002, "msg": "cdk无效"}))

        if cdkInfo.can_use_num != -1 and cdkInfo.can_use_num <= 0:
            return HttpResponse(json.dumps({"code": 18006, "subCode": 18010, "msg": "cdk无剩余次数"}))

        res = models.KbeCdkRecode.objects.filter(dbid=dbid, cdk=cdk)
        if res.count() != 0:
            return HttpResponse(json.dumps({"code": 18006, "subCode": 18001, "msg": "已经领取过"}, ensure_ascii=False), )

        if not cdkInfo.start_time.timestamp() < datetime.now().timestamp() <= cdkInfo.end_time.timestamp():
            return HttpResponse(json.dumps({"code": 18006, "subCode": 18003, "msg": "cdk已过期"}))

        if cdkInfo.code_use_obj != "-1" and str(uuid) not in list(cdkInfo.code_use_obj):
            return HttpResponse(json.dumps({"code": 18006, "subCode": 18009, "msg": "不在cdk可使用对象范围"}))

        item_id = [int(x) for x in re.split(",+|=+", cdkInfo.item_id) if x]
        item_count = [int(x) for x in re.split(",+|=+", cdkInfo.item_count) if x]
        item_info = dict(zip(item_id, item_count))
        cdkInfo.can_use_num -= 1
        cdkInfo.use_num += 1
        cdkInfo.save()

        exchange_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        models.KbeCdkRecode.objects.create(dbid=dbid, name=name, cdk=cdkInfo.activation_code,
                                           create_date=exchange_date)

    except Exception as e:
        HttpResponse(json.dumps({"code": 18007, "subCode": 18004, "msg": "cdk处理失败"}))
        raise e

    return HttpResponse(
        json.dumps(
            {"code": 10000, "subCode": 10000, "msg": "", "dbid": dbid, "uuid": uuid, "cdk": cdkInfo.activation_code,
             "itemInfo": item_info},
            ensure_ascii=False), )


def codeRecord(request):
    """激活码领取记录"""
    if request.method == "GET":
        return render(request, "codeRecord.html")

    uid = request.POST.get("uid")
    code = request.POST.get("code")

    if uid is not None:
        res = game.models.TblAvatar.objects.filter(sm_uuid=uid)
        if res.count() <= 0:
            return HttpResponse(json.dumps({'code': 0, 'count': 1, 'data': 0, "msg": "没有此用户"}, ensure_ascii=False), )
        uInfo = game.models.TblAvatar.objects.get(sm_uuid=uid)

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
            uid = game.models.TblAvatar.objects.get(id=c.dbid).sm_uuid

            arr.append({"name": c.name, "uid": uid, "code": c.cdk, "createTime": str(c.create_date)})
        data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )


def codeRecordInfo(request):
    cdkRecordInfo = models.KbeCdkRecode.objects.all()
    arr = []
    for c in cdkRecordInfo:
        uid = game.models.TblAvatar.objects.get(id=c.dbid).sm_uuid
        arr.append({"name": c.name, "uid": uid, "code": c.cdk, "createTime": str(c.create_date)})
    data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def addActivity(request):
    if request.method == "GET":
        return render(request, "activity_send.html")


# def getActivityReward(request):
#     activityBatch = request.POST.get("activityBatch")
#     data = models.TblActivityReward.objects.filter(activityBatch=activityBatch)
#     res = {}
#     for info in data:
#         res.setdefault(info.rewardid, "奖励id" + ":" + info.rewardid)
#     return HttpResponse(json.dumps(res, ensure_ascii=False), )


def activityInfo(request):
    rewardInfo = json.loads(request.POST.get("rewardInfo"))
    activityInfo = json.loads(request.POST.get("activityInfo"))
    taskRewardInfo = json.loads(request.POST.get("taskRewardInfo"))
    activityTemplateInfo = json.loads(request.POST.get("activityTemplateInfo"))

    templateInfo = {}
    activityBatch = 1
    if models.TblActivityTemplate.objects.count() > 0:
        activityBatch = models.TblActivityTemplate.objects.latest('activitybatch').activitybatch

    for key, tInfo in activityTemplateInfo.items():
        startTime = int(time.mktime(time.strptime(tInfo.get('startTime').strip(), "%Y-%m-%d %H:%M:%S")))  # 转时间戳
        endTime = int(time.mktime(time.strptime(tInfo.get('endTime').strip(), "%Y-%m-%d %H:%M:%S")))  # 转时间戳
        templateInfo[activityBatch] = {'activityBatch': activityBatch, 'templateId': activityBatch,
                                       'activityList': tInfo.get("activityList"),
                                       'extAttr': tInfo.get("extAttr"),
                                       'startTime': startTime, 'endTime': endTime}

        models.TblActivityTemplate.objects.create(activitybatch=activityBatch, templateid=activityBatch,
                                                  activitylist=tInfo.get("activityList"),
                                                  extattr=tInfo.get("extAttr"), starttime=startTime, endtime=endTime)
    activityId = 1
    rewardId = 1
    if models.TblActivity.objects.count() > 0:
        activityId = models.TblActivity.objects.latest('activityid').activityid
    if models.TblActivityReward.objects.count() > 0:
        rewardId = models.TblActivityReward.objects.latest('rewardid').rewardid

    activityInfos = {}
    for key, info in activityInfo.items():
        receiveLimit = info.get("activityLimit")
        if info.get("activityType") == 1 or info.get("activityType") == 4:
            for k, v in info.get("activityLimit").items():
                receiveLimit[int(k) + rewardId] = v

        info_ = {"id_": activityId + 1, "activityBatch": activityBatch, "activityType": info.get("activityType"),
                 'receiveLimit': receiveLimit,
                 'extAttr': info.get("activityGroupList"), 'extAttr2': info.get("extAttrLv")}

        models.TblActivity.objects.create(activityid=activityId + 1, activitybatch=activityBatch,
                                          activitytype=info.get("activityType"),
                                          receivelimit=receiveLimit, extattr=info.get("activityGroupList"),
                                          extattr2=info.get("extAttrLv"), activitytitle=info.get("activityTitle"),
                                          activitytext=info.get("activityText"))
        activityInfos[activityId + 1] = info_
        activityId += 1

    taskInfo = {}
    taskId = 10227
    if models.TblActivityReward.objects.count() > 0:
        taskId = models.TblActivityTask.objects.latest('taskid').taskid

    for key, info in taskRewardInfo.items():
        info_ = {'taskId': taskId + 1, 'activityBatch': activityBatch, 'taskTypeId': 10,
                 'taskSubTypeId': info.get('taskDay'),
                 'itemId': info.get('taskReward'),
                 'itemCount': info.get('taskRewardCount'), 'taskType': info.get('taskTypeId'),
                 'num': info.get('taskNum'),
                 'isStorage': info.get('isStorage')}

        models.TblActivityTask.objects.create(taskid=taskId + 1, activitybatch=activityBatch,
                                              tasktypeid=10,
                                              tasksubtypeid=info.get('taskDay'), itemid=info.get('taskReward'),
                                              itemcount=info.get('taskRewardCount'), tasktype=info.get('taskTypeId'),
                                              num=info.get('taskNum'), isstorage=info.get('isStorage'))

        taskInfo.setdefault(taskId, info_)
        taskId += 1

    activityReward = {}
    for key, info in rewardInfo.items():
        activityReward = {
            info.get("id"): {'id_': rewardId + 1, 'activityType': info.get("activityType"),
                             'activityBatch': activityBatch,
                             'exchangeType': info.get("exchangeItem"), 'exchangeLimit': info.get("exchangeCount"),
                             'itemId': info.get("itemId"), 'itemCount': info.get("itemCount")}}

        models.TblActivityReward.objects.create(rewardid=rewardId + 1, activitytype=info.get("activityType"),
                                                activitybatch=activityBatch,
                                                exchangetype=info.get("exchangeItem"),
                                                exchangelimit=info.get("exchangeCount"),
                                                itemid=info.get('itemId'), itemcount=info.get('itemCount'))

    data = {"activityTemplate": templateInfo,
            "activityTask": taskInfo,
            "activityReward": activityReward,
            "activityInfo": activityInfos,
            }

    val = requestGame(data, settings.GAME_ACTIVITY_SEND)
    # if val['res'] is True:
    #     # 数据库插记录
    #     models.KbeBulletin.objects.create(title=title, message=message, source=source, sendtime=create_time,
    #                                       bulletintype=messageType, state=1)

    return redirect("/operate/addActivity/")


#
# def getTemplateInfo(request):
#     """获取模板信息"""
#     arr = []
#     tInfo = models.TblActivityTemplate.objects.all()
#     for t in tInfo:
#         rewardInfo = {}
#         aInfo = models.TblActivityReward.objects.filter(activitybatch=t.templateid)
#         for a in aInfo:
#             rewardInfo = {}
#
#     data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
#     return HttpResponse(json.dumps(data, ensure_ascii=False), )


def getInActivity(request):
    newTime = time.time()
    tInfos = models.TblActivityTemplate.objects.filter(endtime__gte=newTime, starttime__lte=newTime).all()

    templateInfo = {}
    activityInfo = {}
    rewardInfo = {}
    taskInfo = {}
    for t in tInfos:
        templateInfo[t.activitybatch] = {'activityBatch': t.activitybatch, 'templateId': t.activitybatch,
                                         'activityList': t.activitylist, 'extAttr': t.extattr,
                                         'startTime': t.starttime, 'endTime': t.endtime}
        aInfos = models.TblActivity.objects.filter(activitybatch=t.activitybatch).all()
        rInfos = models.TblActivityReward.objects.filter(activitybatch=t.activitybatch).all()
        tInfos = models.TblActivityTask.objects.filter(activitybatch=t.activitybatch).all()
        for a in aInfos:
            activityInfo[a.activityid] = {'id_': a.activityid, 'activityBatch': a.activitybatch,
                                          'activityType': a.activitytype, 'receiveLimit': a.receivelimit,
                                          'extAttr': a.extattr, 'extAttr2': a.extattr2}

        for r in rInfos:
            rewardInfo[r.rewardid] = {'id_': r.rewardid, 'activityType': r.activitytype,
                                      'activityBatch': r.activitybatch, 'exchangeType': r.exchangetype,
                                      'exchangeLimit': r.exchangelimit,
                                      'itemId': r.itemid, 'itemCount': r.itemcount}

        for t in tInfos:
            taskInfo[t.taskid] = {'taskId': t.taskid, 'activityBatch': t.activitybatch, 'taskTypeId': t.tasktypeid,
                                  'taskSubTypeId': t.tasksubtypeid, 'itemId': t.itemid,
                                  'itemCount': t.itemcount, 'taskType': t.tasktype, 'num': t.num,
                                  'isStorage': t.isstorage}

    data = {"activityTemplate": templateInfo,
            "activityTask": taskInfo,
            "activityReward": rewardInfo,
            "activityInfo": activityInfo,
            }
    val = requestGame(data, settings.GAME_ACTIVITY_SEND)
    # if val['res'] is True:
    #     # 数据库插记录
    #     models.KbeBulletin.objects.create(title=title, message=message, source=source, sendtime=create_time,
    #                                       bulletintype=messageType, state=1)


def addActivityTemplate(request):
    """添加新一期活动"""
    if request.method == 'GET':
        return render(request, "add_activity_template.html")

    activityBatch = 1
    if models.TblActivityTemplate.objects.count() > 0:
        activityBatch = models.TblActivityTemplate.objects.latest('activitybatch').activitybatch + 1
    templateInfo = json.loads(request.POST.get("templateInfo"))

    startTime = int(time.mktime(time.strptime(templateInfo.get('startTime').strip(), "%Y-%m-%d %H:%M:%S")))  # 转时间戳
    endTime = int(time.mktime(time.strptime(templateInfo.get('endTime').strip(), "%Y-%m-%d %H:%M:%S")))  # 转时间戳

    models.TblActivityTemplate.objects.create(activitybatch=activityBatch, templateid=1,
                                              activitylist=templateInfo.get("activityList"),
                                              extattr=templateInfo.get("extAttr"), starttime=startTime, endtime=endTime)

    data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': []}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def activityTemplateInfo(request):
    """每期活动基本信息"""
    arr = []
    infos = models.TblActivityTemplate.objects.all()
    if infos.count() <= 0:
        data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )

    for i in infos:
        activityList = []
        extAttr = []
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.starttime))
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.endtime))

        activityInfo = []
        for activity in json.loads(i.activitylist):
            a = {1: "任务", 2: "捐赠", 3: "掉落", 4: "兑换"}
            activityList.append(a.get(int(activity)))
            activityInfo.append({int(activity): a.get(int(activity))})

        i_data = i.extattr.replace("'", "").replace("[", "").replace("]", "").split(",")
        itemList = [int(d) for d in i_data]
        itemInfo = []
        for itemId in itemList:
            if d_item.datas.get(int(itemId)) is None:
                continue
            extAttr.append(d_item.datas.get(int(itemId)).get("name"))
            itemInfo.append({int(itemId): d_item.datas.get(int(itemId)).get("name")})

        arr.append({'activityBatch': i.activitybatch, 'templateId': i.templateid, 'activityList': activityList,
                    'extAttr': extAttr, 'startTime': startTime, 'endTime': endTime, "activityInfo": activityInfo,
                    "itemInfo": itemInfo})

    data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def addActivityReward(request):
    """添加活动奖励"""
    if request.method == "GET":
        return render(request, "add_activity_reward.html")
    activityBatchId = request.POST.get("activityBatchId")
    activityType = request.POST.get("activityType")
    exchangeType = request.POST.get("exchangeType")
    exchangeLimit = request.POST.get("exchangeLimit")
    itemId = request.POST.get("itemId")
    itemCount = request.POST.get("itemCount")

    rewardId = models.TblActivityReward.objects.latest('rewardid').rewardid + 1
    models.TblActivityReward.objects.create(rewardid=rewardId, activitybatch=activityBatchId,
                                            activitytype=activityType,
                                            exchangetype=exchangeType, exchangelimit=exchangeLimit, itemid=itemId,
                                            itemcount=itemCount)
    data = {'code': 0, 'msg': '添加成功', 'count': 0, 'data': []}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def activityReward(request):
    """活动奖励信息"""
    arr = []
    rewardInfo = models.TblActivityReward.objects.all()
    if rewardInfo.count() <= 0:
        data = {'code': 0, 'msg': 'OK', 'count': 0, 'data': arr}
        return HttpResponse(json.dumps(data, ensure_ascii=False), )
    for reward in rewardInfo:
        a = {1: "任务", 2: "捐赠", 3: "掉落", 4: "兑换"}
        item = d_item.datas.get(int(reward.itemid)).get("name")
        exchangeType = ""
        activityType = a.get(int(reward.activitytype))
        if len(reward.exchangetype) > 0:
            exchangeType = d_item.datas.get(int(reward.exchangetype)).get("name")

        arr.append(
            {"rewardId": reward.rewardid, "activityType": activityType, "activityBatch": reward.activitybatch,
             "exchangeType": exchangeType, "exchangeLimit": reward.exchangelimit, "itemId": item,
             "itemCount": reward.itemcount
             })

    data = {'code': 0, 'msg': 'OK', 'count': len(arr), 'data': arr}
    return HttpResponse(json.dumps(data, ensure_ascii=False), )


def requestGame(data, route):
    info = json.dumps(data)

    url = settings.GAME_SERVER_URL_ORIGINS + settings.GAME_SERVER_ROUTE_ORIGINS.get(route)
    headers = settings.GAME_SERVER_HEADER_ORIGINS
    data = bytes(info, encoding="utf-8")
    res = urllib.request.Request(url, data, headers)

    try:
        response = urllib.request.urlopen(res, timeout=3)
    except:
        return {"res": False, "message": '发送超时!'}

    val = response.read().decode("utf-8")
    val = json.loads(val)

    return val


def game_version_info(request):
    return render(request, "game_version.html")


class FileUploadForm(forms.Form):
    file = forms.FileField(label="文件上传")


def handle_uploaded_file(f):
    save_path = os.path.join('../', f.name)
    with open(save_path, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)

    return save_path, f.name


@csrf_exempt
def game_version_upload(request):
    """
    上传版本文件
    """
    save_path = ""
    if request.method == 'POST':
        forms = FileUploadForm(request.POST, request.FILES)
        if forms.is_valid():
            save_path, file_name = handle_uploaded_file(request.FILES['file'])
            cos_client.upload_file('wegame-1257128478', save_path, file_name)
            return HttpResponse(
                json.dumps({'code': 0, 'msg': '上传成功', 'data': {'src': save_path}}, ensure_ascii=False), )
    else:
        return HttpResponse(
            json.dumps({'code': 1, 'msg': '上传失败', 'data': {'src': save_path}}, ensure_ascii=False), )
    pass
