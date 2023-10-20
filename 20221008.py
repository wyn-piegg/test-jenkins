{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->
{% block head %}
    <link href="{% static 'plugins/daterangepicker-master/daterangepicker.css' %}" rel="stylesheet">
    <link href="{% static '/layui/css/layui.css' %}" type="text/css" rel="stylesheet">
{% endblock %}

{% block content %}
    <!-- Modal -->


    <form class="layui-form" id="notarize" style="display:none" lay-filter="notarize">
        <div class="layui-form-item" id="add_info_div">
            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                <div class="layui-input-block">

                </div>
                确认公告标题：<input type="text" name="formTitle" id="formTitle" autocomplete="off"
                              placeholder=""
                              class="layui-input">

                <div class="layui-input-block">

                </div>

                确认公告内容：<input type="text" name="formText" id="formText" autocomplete="off"
                              placeholder=""
                              class="layui-input">
                <div class="layui-input-block">

                </div>
                确认公告时间：<input type="text" name="formTime" id="formTime" autocomplete="off"
                              placeholder=""
                              class="layui-input">
                <div class="layui-input-block">

                </div>
                确认公告类型：<input type="text" name="formType" id="formType" autocomplete="off"
                              placeholder=""
                              class="layui-input">
                <div class="layui-input-block">

                </div>

                确认口令：<input type="text" name="affirm_info" id="affirm_info" autocomplete="off"
                            placeholder="请输入moshi确认发送公告"
                            class="layui-input">

                <div class="layui-input-block">

                </div>

                <button class="layui-btn" type="submit" lay-submit lay-filter="btnSubmit" id="btnSubmit">
                    确认无误提交
                </button>


            </div>
        </div>
    </form>




    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <form id="message_info">
                    {% csrf_token %}
                    <div class="col-lg-7" style="margin: 0 auto">
                        <div class="card-title">
                            <h2 style=" text-align: center;color: #448AFF">添加公告</h2>
                        </div>
                        <div class="card-body">
                            <div class="list-group">
                                <div class="form-group">
                                    <label style="font-size: 16px">标题</label>
                                    <textarea class="form-control" placeholder="公告标题" id="titleText"
                                              name="title"></textarea>
                                </div>
                                <div class="form-group">
                                    <label style="font-size: 16px">内容</label>
                                    <textarea class="form-control" placeholder="公告内容" id="context" name="message"
                                              style="vertical-align:top;outline:none;height: 150px"></textarea>
                                </div>
                                <div class="form-group">
                                    <label style="font-size: 16px">发送时间</label>
                                    <input type="text" placeholder="发送时间" id="sendTime" name="sendTime"
                                           class="form-control" style="text-align: center" required>
                                </div>
                                <div class="form-group">
                                    <select name="messageType"
                                            style="vertical-align:top;outline:none;height: 50px;width: 100%;text-align: center"
                                            id="selectType">
                                        <option value="1">维护公告</option>
                                        <option value="2">更新公告</option>
                                        <option value="3">活动公告</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="btn btn-primary btn-group-right" onclick="active_query()" id="addText"
                            style="border: 1px solid ;width: 350px;margin-left: 30%;margin-right: auto" type="button">
                        <i class="ti-mouse-alt" href="uidModal">添加</i>
                    </button>
                </form>

            </div>
        </div>
    </div>

    <table class="layui-hide" id="users" lay-filter="test"></table>


{% endblock %}

{% block js %}
    <script src="{% static 'plugins/daterangepicker-master/moment.min.js' %}"></script>
    <script src="{% static 'plugins/daterangepicker-master/daterangepicker.js' %}"></script>
    <script src="{% static 'layui/layui.js' %}" charset="utf-8"></script>
    <script type="text/javascript">
        layui.use(['form', 'table', "laydate", 'layer'], function () {
            var table = layui.table;
            var form = layui.form;
            var layer = layui.layer;
            var laydate = layui.laydate;
            var $ = layui.$;

            $("#addText").on('click', function () {
                layer.open({
                    type: 1,
                    content: $("#notarize"), //这里content是一个普通的String
                    area: ["900px", '800px'],
                    success: function () {
                        var mayselect = document.getElementById("selectType")
                        var index = mayselect.selectedIndex

                        var titleText = document.getElementById("titleText").value
                        var context = document.getElementById("context").value
                        var sendTime = document.getElementById("sendTime").value
                        var textType = mayselect.options[index].text
                        form.val("notarize", {
                            "formTitle": titleText,
                            "formText": context,
                            "formTime": sendTime,
                            "formType": textType,
                        })
                    }
                })
            });

            $("#btnSubmit").on('click', function () {
                if ($("#affirm_info").val() !== 'moshi') {
                    alert("请正确输入口令：moshi")
                    return false
                } else {
                    $.ajax({
                        url: "/message/send/", //url
                        type: "post",//方法类型
                        dataType: "JSON",//预期服务器返回的数据类型
                        data: $('#message_info').serialize(),
                        success: function (res) {
                            // 将后台返回的数据，更新到option中
                            // 使用刚指定的配置项和数据显示图表。
                            if (res.res) {
                                open()
                                alert(res.message)
                            } else {

                            }
                        }
                    })
                }

            });
            $.ajaxSetup({
                data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
            })

            var res = true

            $(function () {
                $('input[name="sendTime"]').daterangepicker({
                    timePicker: true,//可选中时分 默认false
                    timePicker24Hour: true,//设置小时为24小时制 默认false
                    singleDatePicker: true,//单日历
                    // autoUpdateInput:false,//1.当设置为false的时候,不给与默认值(当前时间)2.选择时间时,失去鼠标焦点,不会给与默认值 默认true
                    startDate: moment().startOf('hour'),
                    endDate: moment().startOf('hour').add(32, 'hour'),
                    ranges: {
                        '今天': [moment().startOf('days'), moment()],
                        '昨天': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                        '近7天': [moment().subtract(7, 'days'), moment()],
                        '这个月': [moment().startOf('month'), moment().endOf('month')],
                        '上个月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                    },

                    locale: {
                        format: 'YYYY-MM-DD HH:mm',
                        separator: " - ",
                        customRangeLabel: "自定义",
                        applyLabel: "确定",
                        cancelLabel: "取消",
                        fromLabel: "起始时间",
                        toLabel: "结束时间",
                        weekLabel: "w",
                        daysOfWeek: ["日", "一", "二", "三", "四", "五", "六"],
                        monthNames: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                    }
                });
            })


        });


    </script>

{% endblock %}