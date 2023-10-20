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
                编号：<input type="text" name="detail_id" id="detail_id" lay-verify="number" autocomplete="off"
                          placeholder=""
                          class="layui-input" readonly="readonly">
            </div>

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                serverId：<input type="text" name="reward_serverId" id="reward_serverId" lay-verify="number"
                                autocomplete="off"
                                placeholder=""
                                class="layui-input" readonly="readonly">
            </div>

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                邮件附件：<input type="text" name="detail_text" id="detail_text"
                            lay-verify="number"
                            autocomplete="off"
                            placeholder=""
                            class="layui-input" readonly="readonly">
            </div>

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                发送时间：<input type="text" name="reward_sendTime" id="reward_sendTime" lay-verify="number"
                            autocomplete="off"
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
                创建时间：<input type="text" name="reward_sTime" id="reward_sTime" lay-verify="number" autocomplete="off"
                            placeholder=""
                            class="layui-input" readonly="readonly">
            </div>

            <div class="layui-input-block">

            </div>
            <div class="layui-input-block">
                状态：<input type="text" name="reward_status" id="reward_status" lay-verify="number" autocomplete="off"
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
                url: '/message/messageInfo/',
                toolbar: '#toolbarDemo',
                cols: [[
                    {field: 'id', title: '编号', width:80, sort: true, fixed: 'left'}
                    , {field: 'serverId', title: 'serverId', width: 80}
                    , {field: 'title', title: '公告标题', width: 200, sort: true}
                    , {field: 'text', title: '公告内容', width: 200, sort: true}
                    , {field: 'textType', title: '公告类型', width: 200, sort: true}
                    , {field: 'sendTime', title: '发送时间', width: 200, sort: true}
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
            table.on('tool(emailInfo)', function (obj) {
                var data = obj.data;
                if (obj.event === 'del') {
                    layer.confirm('真的删除行么', function (index) {
                        layer.close(index);
                        $.ajax({
                            type: "post",
                            url: "/email/info/del",
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
                            form.val("detailForm", {
                                "detail_id": obj.data.id,
                                "reward_serverId": obj.data.serverId,
                                "detail_text": obj.data.text,
                                "reward_sendTime": obj.data.sendTime,
                                "reward_sTime": obj.data.createTime,
                                "reward_eTime": obj.data.endTime,
                                "reward_status": obj.data.status,

                            })
                        }

                    })
                }
            });

        });

    </script>
{% endblock %}