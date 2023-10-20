{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->
{% load poll_extras %}
{% block head %}
    <link href="{% static 'assets/css/lib/jsgrid/jsgrid.min.css' %}" type="text/css" rel="stylesheet">
{% endblock %}

{% block content %}
    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <div style="overflow-y: auto">
                    <table class="table table-bordered table-hover" id="email_table_list">
                        <tbody>
                        <tr>
                            <th>编号</th>
                            <th>serverId</th>
                            <th>接收玩家</th>
                            <th>邮件标题</th>
                            <th>邮件内容</th>
                            <th>附件</th>
                            <th>发送时间</th>
                            <th>截止时间</th>
                            <th>创建时间</th>
                            <th>状态</th>
                            <th>操作</th>
                        </tr>
                        </tbody>
                        <tbody id='email_tbody_list'>
                        {% for obj in page_data %}
                            <tr>
                                <td>{{ obj.id }}</td>
                                <td>1</td>
                                <td>
                            <textarea class="form-control" readonly="readonly" style="background-color: white"
                                      name="player">{{ obj.player|toPlayerLength }}</textarea>
                                </td>
                                <td>{{ obj.title }}</td>
                                <td>
                            <textarea class="form-control" readonly="readonly" style="background-color: white"
                                      name="message">{{ obj.message }}</textarea>
                                </td>
                                <td>
                            <textarea class="form-control" readonly="readonly" style="background-color: white"
                                      name="itemInfo">{{ obj.itemInfo|emailItemInfo }}</textarea>
                                </td>
                                <td>{{ obj.sendTimes }}</td>
                                <td>{{ obj.endTimes }}</td>
                                <td>{{ obj.createtime }}</td>
                                {% if obj.is_confirm == 0 %}
                                    <td>未执行</td>\
                                {% elif obj.is_confirm == 1 %}
                                    <td>已读取</td>
                                {% elif obj.is_confirm == 2 %}
                                    <td>未确认</td>
                                {% elif obj.is_confirm == 3 %}
                                    <td>处理失败</td>
                                {% elif obj.is_confirm == 4 %}
                                    <td>禁用</td>
                                {% elif obj.is_confirm == 5 %}
                                    <td>已删除</td>
                                {% else %}
                                    <td>未知操作</td>
                                {% endif %}
                                <td>
                                    <a href='#' onclick='del_email(this)' id={{ obj.id }} style="color:red">删除 </a>
                                    <a href='#email_dialog' data-toggle='modal' name={{ obj.id }} style="color:#0D47A1">查看</a>
                                </td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="row">
                    <div class="col-lg-12">
                        <ul class="pagination justify-content-end" id="page_info">
                            <li class="page-item disabled">
                                <a class="page-link" href="#" tabindex="-1" aria-disabled="true">首页</a>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- /# card -->
            </div>
        </div>
        <!-- /# column -->
    </div>

    <div aria-hidden="true" role="dialog" tabindex="-1" id="email_dialog" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content text-left">
                <div class="modal-header">
                    <h4 class="modal-title">邮件详情</h4>
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

                        <div class="form-group">
                            <label style="font-size: 16px">过期时间</label>
                            <input type="text" readonly="readonly" id="email_send_endtimes" name="email_send_endtimes"
                                   class="form-control">
                        </div>

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
                    </form>
                </div>
            </div>
        </div>
    </div>
{% endblock %}


{% block js %}
    <script type="text/javascript">
        var cell_map_to_idx = {
            id: 0,
            serverId: 1,
            player: 2,
            title: 3,
            message: 4,
            itemInfo: 5,
            sendTimes: 6,
            endTimes: 7,
            createtime: 8,
            is_confirm: 9,
        }
        var confirm_state = {
            0: '未执行',
            1: '已读取',
            2: '未确认',
            3: '处理失败',
            4: '禁用',
            5: '已删除',
        }

        $(function () {

            var page = document.getElementById("page_info");
            var page_count = Math.ceil({{ total_row }}/ 10);
            setPageCookie({{ curr_page }}, page_count)

            for (var i = 1; i < page_count;) {
                page.innerHTML += "<li class='page-item'><a class='page-link' href='#' id=" + i + " onclick='click_page(this)'>" + i + "</a></li>";
                i++;
            }
            page.innerHTML += "<li class='page-item'><a class='page-link' href='#' onclick='click_next(this)'>下一页</a></li>"
        })


        // 模态框 打开前
        $('#email_dialog').on('shown.bs.modal', function (event) {
            var rowId = event.relatedTarget.name
            var row = document.getElementById(rowId)


            let player = row.parentNode.parentNode.cells[cell_map_to_idx.player].lastElementChild.innerHTML
            document.getElementById("email_send_range").value = player;

            let title = row.parentNode.parentNode.cells[cell_map_to_idx.title].innerText
            document.getElementById("email_send_title").value = title;


            var starttimes_value = row.parentNode.parentNode.cells[cell_map_to_idx.sendTimes].innerText
            document.getElementById("email_send_starttimes").value = starttimes_value;

            var endtimes_value = row.parentNode.parentNode.cells[cell_map_to_idx.endTimes].innerText
            document.getElementById("email_send_endtimes").value = endtimes_value;

            var context_value = row.parentNode.parentNode.cells[cell_map_to_idx.message].lastElementChild.innerHTML
            document.getElementById("email_send_context").value = context_value;

            var str = row.parentNode.parentNode.cells[cell_map_to_idx.itemInfo].lastElementChild.innerHTML
            var row = eval('(' + str + ')')
            var send_row = document.getElementById("email_send_attached");

            for (let key in row) {
                NewRow = send_row.insertRow();
                //添加行
                text = NewRow.insertCell();
                text.innerText = key

                text = NewRow.insertCell();
                text.innerText = row[key].toString()
            }
        })


        // 模态框 关闭前
        $('#email_dialog').on('hide.bs.modal', function () {
            var tbody = document.getElementById("email_send_attached");
            if (tbody.children.length > 0) {
                for (var i = tbody.children.length - 1; i >= 0; i--) {
                    tbody.removeChild(tbody.children[i])
                }
            }
        });


        function setPageCookie(page, row) {
            document.cookie = "curr_page=" + page;
            document.cookie = "total_page=" + row;
        }

        function getPageCookie(name) {
            var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
            if (arr = document.cookie.match(reg))
                return unescape(arr[2]);
            else
                return null;
        }

        function reset_mail_info(res) {
            var tbody = document.getElementById("email_tbody_list");
            var page_count = Math.ceil(res.total_row / 10);
            setPageCookie(res.curr_page, page_count)
            if (tbody.children.length > 0) {
                for (var i = tbody.children.length - 1; i >= 0; i--) {
                    tbody.removeChild(tbody.children[i])
                }
            }

            for (var i = 0; i < res.page_data.length; i++) {
                NewRow = tbody.insertRow();
                var obj = res.page_data[i]
                text = NewRow.insertCell();
                text.innerText = obj.id

                text = NewRow.insertCell();
                text.innerText = 1

                text = NewRow.insertCell();
                console.log(obj.player.length)
                text.innerHTML = "<textarea class='form-control' readonly='readonly' name='player' style='background-color: white'>" + (obj.player.length > 0 ? obj.player.toString() : "全服") + "</textarea>"

                text = NewRow.insertCell();
                text.innerText = obj.title

                text = NewRow.insertCell();
                text.innerHTML = "<textarea class='form-control' readonly='readonly' name='message' style='background-color: white'>" + obj.message + "</textarea>"

                text = NewRow.insertCell();
                var itemInfoStr = "{";
                for (let key in obj.itemInfo) {
                    itemInfoStr += key + ':' + JSON.stringify(obj.itemInfo[key])
                    itemInfoStr += ','
                }
                itemInfoStr += "}";
                text.innerHTML = "<textarea class='form-control' readonly='readonly' name='itemInfo' style='background-color: white'>" + itemInfoStr + "</textarea>"

                text = NewRow.insertCell();
                text.innerText = obj.sendTimes

                text = NewRow.insertCell();
                text.innerText = obj.endTimes

                text = NewRow.insertCell();
                text.innerText = obj.createtime

                text = NewRow.insertCell();
                text.innerText = confirm_state[obj.is_confirm] ?? '未知操作'


                // for (let key in obj) {
                //    if (obj.hasOwnProperty(key)) {
                //        text = NewRow.insertCell();
                //        text.innerText = obj[key].toString()
                //    }
                // }

                handle = NewRow.insertCell()
                handle.innerHTML = "<a href='#' onclick='del_email(this)' id=" + obj.id + " style='color:red'>删除 </a>" +
                    "<a href='#email_dialog' data-toggle='modal' name=" + obj.id + " style='color: #0D47A1'>查看</a>"
            }
        }


        function click_page(obj) {
            curr_page = getPageCookie('curr_page')
            if (curr_page == null) {
                return;
            }

            if (curr_page == obj.id) {
                return
            }

            $.ajax({
                url: "", //url
                type: "post",//方法类型
                dataType: "JSON",//预期服务器返回的数据类型
                data: $.param({curr_page: curr_page, request_page: obj.id}),
                success: function (res) {
                    reset_mail_info(res)
                }
            })
        }

        function click_next(obj) {
            var page = getPageCookie('curr_page')
            var row = getPageCookie('total_page')

            request_page = parseInt(page) + 1

            if (request_page > row) {
                return
            }

            $.ajax({
                url: "", //url
                type: "post",//方法类型
                dataType: "JSON",//预期服务器返回的数据类型
                data: $.param({curr_page: page, request_page: request_page}),
                success: function (res) {
                    reset_mail_info(res)
                }
            })
        }


        function del_email(obj) {

            $.ajax({
                url: "del", //url
                type: "post",//方法类型
                dataType: "JSON",//预期服务器返回的数据类型
                data: $.param({del_id: parseInt(obj.id)}),
                success: function (result) {
                    if (result.res == true) {
                        row = document.getElementById(result.del_id);
                        row.parentNode.parentNode.cells[cell_map_to_idx.is_confirm].innerText = confirm_state[result.is_confirm]
                        {#alert(row)#}
                    }
                }
            })
        }

        function read_email(obj) {
            dialog = document.getElementById("email_dialog")
            // dialog.
            alert(dialog)
        }

    </script>
{% endblock %}