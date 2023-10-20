# {% extends 'layout_left.html' %}
# {% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->
#
# {% block head %}
#     <link href="{% static '/layui/css/layui.css' %}" type="text/css" rel="stylesheet">
# {% endblock %}
#
# {% block content %}
#
#
#     <table class="layui-hide" id="activation" lay-filter="activation"></table>
#
# {% endblock %}
#
# {% block js %}
#
#     <script type="text/html" id="toolbarDemo">
#         <div class="demoTable">
#             用户id：
#             <div class="layui-inline">
#                 <input class="layui-input" type="search" name="userIdInfo" id="userIdInfo" autocomplete="off"
#                        placeholder="输入用户id"
#                        onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"
#                        onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}">
#             </div>
#             <button class="layui-btn" id="select_id_btn" lay-event="select_id_item" type="button"><i class="layui-icon">&#xe615;</i>搜索
#             </button>
#
#             用户昵称：
#             <div class="layui-inline">
#                 <input class="layui-input" type="search" name="userNameInfo" id="userNameInfo" autocomplete="off"
#                        placeholder="输入用户昵称">
#             </div>
#             <button class="layui-btn" id="select_name_btn" lay-event="select_name_item" type="button"><i
#                     class="layui-icon">&#xe615;</i>搜索
#             </button>
#         </div>
#
#         <div class="layui-form-label-col">
#
#         </div>
#
#         <div class="demoTable">
#             时间范围：
#             <div class="layui-inline">
#                 <input class="layui-input" type="search" name="userIdInfo" id="userIdInfo" autocomplete="off"
#                        placeholder="输入用户id"
#                        onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"
#                        onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}">
#             </div>
#             <button class="layui-btn" id="select_id_btn" lay-event="select_id_item" type="button"><i class="layui-icon">&#xe615;</i>搜索
#             </button>
#
#             查询类型：
#             <div class="layui-inline">
#                 <input class="layui-input" type="search" name="userNameInfo" id="userNameInfo" autocomplete="off"
#                        placeholder="输入用户昵称">
#             </div>
#             <button class="layui-btn" id="select_name_btn" lay-event="select_name_item" type="button"><i
#                     class="layui-icon">&#xe615;</i>搜索
#             </button>
#         </div>
#
#         <div class="layui-form-label-col">
#
#         </div>
#
#         <div class="layui-btn-container">
#             <button class="layui-btn layui-btn-sm" lay-event="add">随机激活码</button>
#             <button class="layui-btn layui-btn-sm" lay-event="add1">手动激活码</button>
#         </div>
#
#     </script>
#
#     <script type="text/html" id="barDemo">
#         <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="detail">查看</a>
#     </script>
#
#     <script src="{% static 'layui/layui.js' %}" charset="utf-8"></script>
#     <!-- 注意：如果你直接复制所有代码到本地，上述 JS 路径需要改成你本地的 -->
#     <script>
#
#         layui.use(['form', 'table', "laydate", 'layer'], function () {
#             var table = layui.table;
#             var form = layui.form;
#             var layer = layui.layer;
#             var laydate = layui.laydate;
#             var $ = layui.$;
#
#
#             //方法级渲染
#             table.render({
#                 elem: '#activation',
#                 url: '/cms/operate/activationInfo/',
#                 toolbar: '#toolbarDemo',
#                 cols: [[
#                     {#{field: 'id', title: 'ID', width:80, sort: true, fixed: 'left', totalRowText: '合计：'}#}
#                     {field: 'cdk_title', title: '激活码标题', width: 150},
#                     {field: 'activationCode', title: '激活码', width: 150}
#                     , {field: 'itemId', title: '道具id', width: 200, sort: true}
#                     , {field: 'itemName', title: '道具名称', width: 200, sort: true}
#                     , {field: 'itemCount', title: '道具数量', width: 200, sort: true}
#                     , {
#                         field: 'code_status',
#                         title: '激活码状态',
#                         width: 200,
#                         sort: true,
#                         align: 'center',
#                         templet: function (res) {
#                             let menuId = res.id
#                             if (res.code_status === 1) {
#                                 return "<input type='checkbox' menuId='" + menuId + "' lay-skin='switch' lay-text='启用|禁用' lay-filter='state' checked>"
#                             } else if (res.code_status === 0) {
#                                 return "<input type='checkbox' menuId='" + menuId + "' lay-skin='switch' lay-text='启用|禁用' lay-filter='state'>"
#                             }
#                         }
#                     }
#                     , {field: 'startTime', title: '开始时间', width: 200, sort: true}
#                     , {field: 'endTime', title: '过期时间', width: 200, sort: true}
#                     , {field: 'useNum', title: '已兑换次数', width: 200, sort: true}
#                     , {fixed: 'right', title: '操作', width: 120, align: 'center', toolbar: '#barDemo'}
#
#                 ]],
#                 id: 'testReload',
#                 page: {
#                     layout: ['limit', 'count', 'prev', 'page', 'next', 'skip']
#                     , curr: 1
#                     , groups: 6
#                     , limit: 10
#                 },
#                 even: true, //开启隔行背景
#                 done: function () {
#                     toolbar();
#                 }
#             });
#
#             var itemInfo = JSON.parse(window.localStorage.itemInfo);
#             // 下拉框
#             let str = "<option value='' name='itemName'></option>";
#             for (let i of itemInfo) {
#                 //组装数据
#                 str += "<option value='" + i.itemId + "' name='itemName'>" + i.itemId + ":" + i.name + "</option>";
#             }
#             //jquery赋值方式
#             $("#selectItemName").html(str);
#             $("#selectItemName2").html(str);
#             //重新渲染生效
#             form.render();
#             var myDate = new Date();
#
#             laydate.render({
#                 elem: '#timeScope'
#                 , type: 'datetime'
#                 , range: '~'
#                 , format: 'yyyy-M-d H:m:s'
#                 , min: myDate.toLocaleString()
#             });
#
#
#             laydate.render({
#                 elem: '#timeScope2'
#                 , type: 'datetime'
#                 , range: '~'
#                 , format: 'yyyy-M-d H:m:s'
#                 , min: myDate.toLocaleString()
#             });
#
#
#             //头工具栏事件
#             table.on('toolbar(activation)', function (obj) {//监听的是<table class="layui-hide" id="users" lay-filter="users"></table>
#                 if (obj.event === 'add') {
#                     layer.open({
#                         type: 1,
#                         content: $("#addForm"), //这里content是一个普通的String
#                         area: ["700px", '750px'],//表单大小
#                     })
#                 } else if (obj.event === 'add1') {
#                     layer.open({
#                         type: 1,
#                         content: $("#addForm1"), //这里content是一个普通的String
#                         area: ["700px", '800px'],//表单大小
#                     })
#                 }
#             });
#
#             function toolbar() {
#                 $("#select_btn").on('click', function () {
#                     if ($('#codeInfo').val() === '') {
#                         layui.use('layer', function () {
#                             var layer = layui.layer;
#                             layer.open({
#                                 title: '提示消息',
#                                 content: '查询条件不存在！'
#                             });
#                         });
#                     } else {
#                         table.reload('testReload', {
#                             url: '/cms/operate/selActivationCode/',
#                             where: {'codeInfo': $('#codeInfo').val()},
#                             method: 'get',
#                             page: {
#                                 curr: 1
#                             }
#                         }, 'data')
#                     }
#                 })
#             }
#
#         });
#
#     </script>
# {% endblock %}
