{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->

{% block head %}
    <link href="{% static '/layui/css/layui.css' %}" type="text/css" rel="stylesheet">
{% endblock %}

{% block content %}

    <form class="layui-form" id="detail_form" style="display:none" lay-filter="detailForm">
        <div class="layui-form-item" id="detail_info_div" lay-filter="layuiadmin-form-role">

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                激活码：<input type="text" name="detail_code" id="detail_code" lay-verify="number" autocomplete="off"
                           placeholder=""
                           class="layui-input" readonly="readonly">
            </div>

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                奖励信息：<input type="text" name="reward_info" id="reward_info" lay-verify="number" autocomplete="off"
                            placeholder=""
                            class="layui-input" readonly="readonly">
            </div>

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                激活码状态：<input type="text" name="detail_code_status" id="detail_code_status"
                             lay-verify="number"
                             autocomplete="off"
                             placeholder=""
                             class="layui-input" readonly="readonly">
            </div>
            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                开始时间：<input type="text" name="reward_sTime" id="reward_sTime" lay-verify="number" autocomplete="off"
                            placeholder=""
                            class="layui-input" readonly="readonly">
            </div>
            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                过期时间：<input type="text" name="reward_eTime" id="reward_eTime" lay-verify="number" autocomplete="off"
                            placeholder=""
                            class="layui-input" readonly="readonly">
            </div>
            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                已兑换次数：<input type="text" name="reward_num" id="reward_num" lay-verify="number" autocomplete="off"
                             placeholder=""
                             class="layui-input" readonly="readonly">
            </div>


        </div>
    </form>


    <table class="layui-hide" id="emailInfo" lay-filter="emailInfo"></table>

{% endblock %}

{% block js %}

    <div class="layui-form-item">
        <label class="layui-form-label">开关</label>
        <div class="layui-input-block">
            <input type="checkbox" name="switch" lay-skin="switch" lay-text="启用|禁用" checked>
        </div>
    </div>

    <script type="text/html" id="barDemo">
        <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="detail">查看</a>
        <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
    </script>

    <script src="{% static 'layui/layui.js' %}" charset="utf-8"></script>
    <!-- 注意：如果你直接复制所有代码到本地，上述 JS 路径需要改成你本地的 -->
    <script>

        layui.use(['form', 'table', "laydate", 'layer'], function () {
            var table = layui.table;
            var form = layui.form;
            var layer = layui.layer;
            var laydate = layui.laydate;
            var $ = layui.$;

            //方法级渲染
            table.render({
                elem: '#emailInfo',
                url: '/email/emailInfo/',
                toolbar: '#toolbarDemo',
                cols: [[
                    {#{field: 'id', title: 'ID', width:80, sort: true, fixed: 'left', totalRowText: '合计：'}#}
                    {field: 'id', title: '编号', width: 150}
                    , {field: 'serverId', title: 'serverId', width: 150}
                    , {field: 'title', title: '邮件标题', width: 200, sort: true}
                    , {field: 'text', title: '邮件附件', width: 200, sort: true}
                    , {field: 'sendTime', title: '发送时间', width: 200, sort: true}
                    , {field: 'endTime', title: '过期时间', width: 200, sort: true}
                    , {field: 'createTime', title: '创建时间', width: 200, sort: true}
                    , {field: 'status', title: '状态', width: 200, sort: true}
                    , {fixed: 'right', title: '操作', width: 120, align: 'center', toolbar: '#barDemo'}

                ]],
                id: 'testReload',
                page: {
                    layout: ['limit', 'count', 'prev', 'page', 'next', 'skip']
                    , curr: 1
                    , groups: 6
                    , limit: 10
                },
                even: true, //开启隔行背景
            });


            //监听行工具事件
            table.on('tool(activation)', function (obj) {
                var data = obj.data;
                if (obj.event === 'del') {
                    layer.confirm('真的删除行么', function (index) {
                        obj.del();
                        layer.close(index);
                        $.ajax({
                            type: "get",
                            url: "/operate/delActivationCode/",
                            data: {
                                "del_id": data.id,
                            },
                            dataType: "JSON",
                            success: function (res) { 　 // 请求被成功响应之后会做的事
                                console.log(res)
                            },
                            error: function (err) {
                                console.log(err) 　　    // 请求发生错误时会做的事
                            }
                        });
                    });
                } else if (obj.event === 'detail') {
                    {#if (read != null) read(obj)#}
                    layer.open({
                        type: 1,
                        content: $("#detail_form"),
                        area: ["800px", '700px'],
                        success: function () {
                            var iName = obj.data.itemName.split(',')
                            var iCount = obj.data.itemCount.split(',')
                            var reward = []
                            for (var i = 0; i < iName.length; i++) {
                                reward.push([iName[i] + " * " + iCount[i]])
                            }
                            var statusDict = {0: "已禁用", 1: "正在使用", 3: "已删除"}
                            form.val("detailForm", {

                                "detail_code": obj.data.activationCode,
                                "reward_info": reward,
                                "detail_item_count": obj.data.itemCount,
                                "detail_code_status": statusDict[obj.data.code_status],
                                "reward_sTime": obj.data.startTime,
                                "reward_eTime": obj.data.endTime,
                                "reward_num": obj.data.useNum,

                            })
                        }

                    })
                }
            });

        });

    </script>
{% endblock %}