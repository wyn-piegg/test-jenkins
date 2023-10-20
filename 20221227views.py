{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->

{% block head %}
    <link href="{% static 'plugins/daterangepicker-master/daterangepicker.css' %}" rel="stylesheet">
    <link href="{% static '/layui/css/layui.css' %}" type="text/css" rel="stylesheet">
{% endblock %}


{% block content %}
    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <form id='query_from' method="post" autocomplete="off">
                    {% csrf_token %}
                    <div class="col-lg-7" style="margin: 0 auto">
                        <div class="form-group">
                            <input type="radio" name="email_type" value="1" id="all" onclick="email_type_all()"><label
                                for="all">全服</label>
                            <input type="radio" name="email_type" value="2" id="single" checked="checked"
                                   onclick="email_type_single()"><label for="single">单人</label>
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">玩家uid(点击输入框)</label>
                            <input href="#uidModal" data-toggle="modal" type="text" readonly="readonly" id="uid_edit"
                                   placeholder="玩家uid" name="uid"
                                   class="form-control">
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">邮件标题</label>
                            <input type="text" placeholder="邮件标题" id="title" name="title" class="form-control">
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">发送时间</label>
                            <input type="text" placeholder="发送时间" id="starttimes" name="starttimes"
                                   class="form-control">
                        </div>
                        {##}
                        {#                        <div class="form-group">#}
                        {#                            <label style="font-size: 16px">过期时间</label>#}
                        {#                            <input type="text" placeholder="过期时间" id="endtimes" name="endtimes" class="form-control">#}
                        {#                        </div>#}

                        <div class="form-group">
                            <label style="font-size: 16px">邮件内容</label>
                            <textarea class="form-control" placeholder="邮件内容" id="context" name="context"></textarea>
                        </div>

                        <label style="font-size: 16px"> 附件 </label>
                        {#                        <a href="#itemModal" data-toggle="modal" title="添加道具"#}
                        {#                           class="btn btn-primary btn-outline m-b-10 m-l-5 h1 small">#}
                        <button type="button" class="layui-btn" id="addItem" name="addItem">添加道具</button>

                        <div class="form-group">
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <tbody>
                                    <tr>
                                        <th>编号</th>
                                        <th>道具ID</th>
                                        <th>道具名称</th>
                                        <th>道具数量</th>
                                        <th>操作</th>
                                    </tr>
                                    </tbody>
                                    <tbody id='attached'>
                                    {#                                    {% for obj in hero_info %}#}
                                    {#                                        <tr>#}
                                    {#                                            <th scope="row">1</th>#}
                                    {#                                            <th>{{ obj.sm_heroid }}</th>#}
                                    {#                                            <th>{{ obj.sm_lv }}</th>#}
                                    {#                                            <th>{{ obj.sm_runes }}</th>#}
                                    {#                                        </tr>#}
                                    {#                                    {% endfor %}#}
                                    </tbody>
                                    <!--                                <input type="button" id="bn" value="add" onclick="add_item_row()"/>-->

                                </table>
                            </div>
                        </div>

                        <a href="#sendModal" data-toggle="modal" title="发送邮件" class="btn btn-compose">发送邮件</a>

                    </div>
                </form>
            </div>
        </div>
    </div>


    <!-- Modal -->
    <div aria-hidden="true" role="dialog" tabindex="-1" id="uidModal" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content text-left">
                <div class="modal-header">
                    <h4 class="modal-title">添加玩家</h4>
                    <button aria-hidden="true" data-dismiss="modal" class="close" type="button"><i class="ti-close"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <label class="col-lg-3 control-label">玩家uid</label>
                    <div class="col-lg-10">
                        <input type="text" placeholder="" id="user_uid" class="form-control">
                        <span type="text" id="uid_error" style="color: red;"></span>
                    </div>
                    <button class="btn btn-primary" data-dismiss="modal" onclick="add_user()">添加</button>
                </div>
            </div>
        </div>
    </div>


    <form class="layui-form" id="item_from" style="display:none" lay-filter="scoreRuleForm" method="post">
        <div class="form-group">
            <label class="col-lg-3 control-label">道具名称</label>
            <div class="col-lg-10">
                <select name="item_name" lay-verify="required"
                        lay-filter="item_name" lay-search
                        id='item_name'>
                    <option value='' name='itemName'></option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label class="col-lg-3 control-label">道具数量</label>
            <div class="col-lg-10">
                <input type="text" placeholder="" id="itemCount" class="form-control" required value=""
                       onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"
                       onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}">
            </div>
        </div>
        <div class="form-group">
            <button type="button" class="layui-btn" id="addEmailItem"> 添加</button>
        </div>

        {#onclick="add_item_info()" #}
    </form>


    {#    <div aria-hidden="true" role="dialog" tabindex="-1" id="itemModal" class="modal fade">#}
    {#        <div class="modal-dialog">#}
    {#            <div class="modal-content text-left">#}
    {#                <div class="modal-header">#}
    {#                    <h4 class="modal-title">添加道具</h4>#}
    {#                    <button aria-hidden="true" data-dismiss="modal" class="close" type="button"><i class="ti-close"></i>#}
    {#                    </button>#}
    {#                </div>#}
    {#                <div class="modal-body">#}
    {#                    <form id="item_from" class="layui-form" autocomplete="off">#}
    {#                        <div class="form-group">#}
    {#                            <label class="col-lg-3 control-label">道具名称</label>#}
    {#                            <div class="col-lg-10">#}
    {#                                <input type="text" placeholder="" id="itemName" name="itemName" class="form-control">#}
    {#                                <select#}
    {#                                        style="vertical-align:top;outline:none;height: 50px;width: 100%;text-align: center"#}
    {#                                        id='item_name'>#}
    {#                                    <option name="itemName" value="-1">道具选择</option>#}
    {#                                </select>#}
    {#                            </div>#}
    {#                        </div>#}
    {#                        <div class="form-group">#}
    {#                            <label class="col-lg-3 control-label">道具Id</label>#}
    {#                            <div class="col-lg-10">#}
    {#                                <input type="text" readonly="readonly" placeholder="" id="itemId" class="form-control"#}
    {#                                       value="-1">#}
    {#                            </div>#}
    {#                        </div>#}
    {#                        <div class="form-group">#}
    {#                            <label class="col-lg-3 control-label">道具数量</label>#}
    {#                            <div class="col-lg-10">#}
    {#                                <input type="text" placeholder="" id="itemCount" class="form-control" required value=0#}
    {#                                       onkeyup="this.value = this.value.replace(/^\D*([0-9]\d*\.?\d{0,2})?.*$/,'$1');">#}
    {#                            </div>#}
    {#                        </div>#}
    {#                    </form>#}
    {#                    <button class="btn btn-primary" data-dismiss="modal" onclick="add_item_info()"> 添加</button>#}
    {#                </div>#}
    {#            </div>#}
    <!-- /.modal-content -->
    {#        </div>#}
    <!-- /.modal-dialog -->
    {#    </div>#}


    <div aria-hidden="true" role="dialog" tabindex="-1" id="sendModal" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content text-left">
                <div class="modal-header">
                    <h4 class="modal-title">确认发送</h4>
                    <button aria-hidden="true" data-dismiss="modal" class="close" type="button"><i class="ti-close"></i>
                    </button>
                </div>

                <div class="modal-body">
                    <form id="send_from" class="form-horizontal" autocomplete="off">
                        <div class="form-group">
                            <label style="font-size: 16px">邮件类型</label>
                            <input type="text" readonly="readonly" placeholder="" id="email_send_type"
                                   name="email_send_type" class="form-control" value="" data-value="">
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">发送范围</label>
                            <input type="text" readonly="readonly" placeholder="" id="email_send_range"
                                   name="email_send_range"
                                   class="form-control">
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">邮件标题</label>
                            <input type="text" readonly="readonly" id="email_send_title" name="email_send_title"
                                   class="form-control">
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">发送时间</label>
                            <input type="text" readonly="readonly" id="email_send_starttimes"
                                   name="email_send_starttimes"
                                   class="form-control">
                        </div>
                        {##}
                        {#                        <div class="form-group">#}
                        {#                            <label style="font-size: 16px">过期时间</label>#}
                        {#                            <input type="text" readonly="readonly" id="email_send_endtimes" name="email_send_endtimes"#}
                        {#                                   class="form-control">#}
                        {#                        </div>#}

                        <div class="form-group">
                            <label style="font-size: 16px">邮件内容</label>
                            <textarea class="form-control" readonly="readonly" id="email_send_context"
                                      name="email_send_context"></textarea>
                        </div>

                        <div class="form-group">
                            <label style="font-size: 16px">邮件附件</label>
                            <div class="form-group">
                                <div class="table-responsive">
                                    <table class="table table-bordered">
                                        <tbody>
                                        <tr>
                                            <th>编号</th>
                                            <th>道具ID</th>
                                            <th>道具名称</th>
                                            <th>道具数量</th>
                                        </tr>
                                        </tbody>
                                        <tbody id='email_send_attached'>
                                        <tr>
                                        </tr>
                                        </tbody>
                                        <!--                                <input type="button" id="bn" value="add" onclick="add_item_row()"/>-->
                                    </table>
                                </div>
                            </div>
                        </div>
                        <button class="btn btn-primary btn-group-right" data-dismiss="modal" type="button"
                                onclick="send_email()">
                            <i class="ti-search"></i>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

{% endblock %}


{% block js %}
    <script src="{% static 'plugins/daterangepicker-master/moment.min.js' %}"></script>
    <script src="{% static 'plugins/daterangepicker-master/daterangepicker.js' %}"></script>
    <script src="{% static 'layui/layui.js' %}" charset="utf-8"></script>

    <script type="text/javascript">
        layui.use(['form', 'table', "laydate", 'layer'], function () {
            var form = layui.form;
            // select组件对象
            var itemInfo = JSON.parse(window.localStorage.itemInfo);
            {#var selectId = document.getElementById("item_name");#}


            let str = "<option value='' name='itemName'></option>";
            for (let i of itemInfo) {
                //组装数据
                str += "<option value='" + i.itemId + "' name='itemName'>" + i.itemId + ":" + i.name + "</option>";
            }

            $("#item_name").html(str);
            form.render();


            $('#addItem').on('click', function () {
                layer.open({
                    type: 1,
                    content: $("#item_from"),
                    area: ["500px", "400px"]
                })
            })

            $('#addEmailItem').on('click', function () {

                var mayselect = document.getElementById("item_name");
                var elements = new Array();
                var index = mayselect.selectedIndex

                var itemIdName = mayselect.options[index].text
                var itemName = itemIdName.substr(itemIdName.indexOf(":") + 1, itemIdName.length)
                var count = document.getElementById("itemCount").value;

                if ($("#itemCount").val() === '') {
                    alert('道具数量错误')
                    return
                } else if ($("#item_name").val() === '') {
                    alert("请选择道具")
                    return
                }
                elements.push(mayselect.value);
                elements.push(itemName)
                elements.push(count);

                if (elements.length > 0) {
                    add_item_row(elements)
                }
                $("#item_from")[0].reset()
                layer.closeAll()
            })


            $(function () {
                $('input[name="starttimes"]').daterangepicker({
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


                $('input[name="endtimes"]').daterangepicker({
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
                selectInit()
            })

            function request_item_info() {
                $.ajax({
                    url: "", // url
                    type: "post",//方法类型
                    dataType: "JSON",//预期服务器返回的数据类型
                    data: "",
                    success: function (res) {
                        // 将后台返回的数据，更新到option中
                        // 使用刚指定的配置项和数据显示图表。
                    }
                })
            }

            function set_item_info() {

            }

            function get_item_info() {

            }

            // 模态框 打开前
            $('#sendModal').on('shown.bs.modal', function (event) {
                var radio_list = document.getElementsByName("email_type")

                var radio_value = -1

                for (var i = 0; i < radio_list.length; i++) {
                    if (radio_list[i].checked === true) {
                        radio_value = radio_list[i].value
                    }
                }

                var uid_value = document.getElementById("uid_edit").value;
                if (radio_value === "1") {
                    document.getElementById("email_send_type").value = "全服"
                } else if (radio_value === "2") {
                    if (uid_value.length <= 0) {
                        alert("个人邮件发送人不能为空");
                        return;
                    }
                    document.getElementById("email_send_type").value = "个人"
                } else {
                    alert("邮件类型错误");
                    return
                }
                document.getElementById("email_send_type").data_value = radio_value


                document.getElementById("email_send_range").value = uid_value;

                var title_value = document.getElementById("title").value;
                document.getElementById("email_send_title").value = title_value;

                var starttimes_value = document.getElementById("starttimes").value;
                document.getElementById("email_send_starttimes").value = starttimes_value;

                {#var endtimes_value = document.getElementById("endtimes").value;#}
                {#document.getElementById("email_send_endtimes").value = endtimes_value;#}

                var context_value = document.getElementById("context").value;
                document.getElementById("email_send_context").value = context_value;

                var row = document.getElementById("attached").rows;
                var send_row = document.getElementById("email_send_attached");
                if (row.length > 0) {
                    for (var i = 0; i < row.length; i++) {
                        NewRow = send_row.insertRow();                        //添加行
                        for (var j = 0; j < 4; j++) {
                            text = NewRow.insertCell();
                            text.innerText = row[i].cells[j].innerText
                        }
                    }
                }

            })

            // 模态框 关闭前
            $('#sendModal').on('hide.bs.modal', function () {
                var tbody = document.getElementById("email_send_attached");
                if (tbody.children.length > 0) {
                    for (var i = tbody.children.length - 1; i >= 0; i--) {
                        tbody.removeChild(tbody.children[i])
                    }
                }
            });

            $('#uidModal').on('hide.bs.modal', function () {
                var input = document.getElementById("user_uid");
                input.value = ""

            });
            {##}
            {#$('#itemModal').on('hide.bs.modal', function () {#}
            {#    document.getElementById("item_from").reset();#}
            {#    var input = document.getElementById("user_uid");#}
            {#    input.value = ""#}
            {##}

            // });

            function email_type_all() {
                var edit = document.getElementById("uid_edit");
                edit.disabled = true
            }

            function email_type_single() {
                var edit = document.getElementById("uid_edit");
                edit.disabled = false
            }


            function add_user() {
                var edit = document.getElementById("uid_edit");
                var original_uid = edit.value
                var add = document.getElementById("user_uid")

                if (add.value == '' || add.value == undefined || add.value == null) {
                    var text = document.getElementById("uid_error");
                    text.textContent = "uid不能为空"
                    return
                }

                var new_uid = add.value
                var new_uid_str = new_uid.concat(";")
                var original_uid_str = original_uid.concat(new_uid_str)
                edit.value = original_uid_str
            }

            //初始化行,设置序列号;
            function initRows(tab) {
                var tabRows = tab.rows.length;
                for (var i = 0; i < tabRows;) {
                    tab.rows[i].cells[0].innerText = ++i;
                }
            }

            function add_item_row(elements) {
                var tab = document.getElementById("attached");   //取得自定义的表对象
                NewRow = tab.insertRow();                        //添加行
                num = NewRow.insertCell();                                // 编号站位
                for (var i = 0; i < elements.length; i++) {
                    text = NewRow.insertCell();
                    text.innerText = elements[i]
                }
                handle = NewRow.insertCell()
                handle.innerHTML = "<a href='#' onclick='del_item_row(this)'>删除</a>"
                initRows(tab)
            }

            function del_item_row(row) {
                var tab = document.getElementById("attached");   //取得自定义的表对象
                var tr = row.parentNode.parentNode;
                tr.parentNode.removeChild(tr);
                initRows(tab)
            }


            {#function add_item_info() {#}
            {#    var from = document.getElementById("item_from");#}
            {#    var elements = new Array();#}
            {#    var tagElements = from.getElementsByTagName('input');#}
            {#    var selectId = document.getElementById("item_name");#}
            {##}
            {#debugger#}
            {#    if (Number(itemId) < 0) {#}
            {#        alert('道具Id错误')#}
            {#        return#}
            {#    }#}
            {#    var count = Number(tagElements.itemCount.value)#}
            {#    if (Number(count) <= 0) {#}
            {#        alert('道具数量错误')#}
            {#        return#}
            {#    }#}
            {#    elements.push(tagElements.itemId.value);#}
            {#    elements.push(selectId.options[selectId.selectedIndex].innerHTML)#}
            {#    elements.push(count);#}
            {#    if (elements.length > 0) {#}
            {#        add_item_row(elements)#}
            {#    }#}
            {#    document.getElementById("itemId").setAttribute("value", -1)#}
            {##}

            //}

            function send_email() {
                var row = document.getElementById("attached").rows;
                var data = [];
                if (row.length > 0) {
                    for (var i = 0; i < row.length; i++) {
                        var itemId = row[i].cells[1].innerText;
                        var count = row[i].cells[3].innerText;
                        data.push({[itemId]: count})
                    }
                }
                if (document.getElementById("email_send_title").value.length <= 0 || document.getElementById("email_send_title").value.length > 10) {
                    alert('标题错误超过最大字符')
                    return
                }
                {#if (document.getElementById("email_send_context").value.length <= 0 || document.getElementById("email_send_context").value.length > 50) {#}
                {#    alert('内容错误超过最大字符')#}
                {#    return#}
                //}

                document.getElementById("email_send_type").value = document.getElementById("email_send_type").data_value
                var item_data = JSON.stringify(data);
                $.ajax({
                    url: "", // url
                    type: "post",//方法类型
                    dataType: "JSON",//预期服务器返回的数据类型
                    data: $('#send_from').serialize() + '&' + $.param({email_send_attached: item_data}),
                    success: function (res) {
                        // 将后台返回的数据，更新到option中
                        // 使用刚指定的配置项和数据显示图表。
                        alert(res.message)
                    }
                })
            }

            // select改变事件
            selectId.onchange = function ()//触发事件
            {
                var result = selectId.options[selectId.selectedIndex].value;
                var input = document.getElementById("itemId");
                input.setAttribute("value", result);
            }

            function selectInit() {
                //下拉菜单
                var storage = window.localStorage;
                if (storage.itemInfo.length > 0) {
                    var newObject = JSON.parse(storage.itemInfo);
                    var tbody = document.getElementById("item_name");
                    var addOption1 = function (select, txt, value, num) {
                        select.add(new Option(txt, value), num);
                    }

                    for (var i = 0; i < newObject.length; i++) {
                        addOption1(tbody, newObject[i].name, newObject[i].itemId)

                    }
                }
            };


            $('input[name="starttimes"]').on('apply.daterangepicker', function (ev, picker) {
                var startTime = new Date(picker.startDate.format('YYYY-MM-DD'))
                var nowTime = new Date()
                if (startTime < nowTime) {
                    Y = nowTime.getFullYear() + '-';
                    M = (nowTime.getMonth() + 1 < 10 ? '0' + (nowTime.getMonth() + 1) : nowTime.getMonth() + 1) + '-';
                    D = nowTime.getDate() + ' ';
                    h = (nowTime.getHours() + 1 <= 24 ? (nowTime.getHours() + 1) : nowTime.getHours()) + ':';
                    m = nowTime.getMinutes();
                    s = nowTime.getSeconds();
                    timeStr = Y + M + D + h + m
                    $('input[name="starttimes"]').data('daterangepicker').setStartDate(timeStr);
                }
            });
        });

    </script>
{% endblock %}