{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->

{% block head %}
    <link href="{% static 'assets/css/lib/jsgrid/jsgrid.min.css' %}" type="text/css" rel="stylesheet">
{% endblock %}

{% block content %}
    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <div style="overflow-y: auto">
                    <table class="table table-bordered table-hover" id="message_table_list">
                        <tbody>
                        <tr>
                            <th>编号</th>
                            <th>serverId</th>
                            <th>公告标题</th>
                            <th>公告内容</th>
                            <th>公告类型</th>
                            <th>发送时间</th>
                            <th>状态</th>
                            <th>操作</th>
                        </tr>
                        </tbody>
                        <tbody id='message_tbody_list'>
                        {% for obj in page_data %}
                            <tr>
                                <td>{{ obj.id }}</td>
                                <td>1</td>
                                <td>{{ obj.title }}</td>
                                <td>
                            <textarea class="form-control" readonly="readonly" style="background-color: white"
                                      name="message">{{ obj.message }}</textarea>
                                </td>
                                {% if obj.bulletinType == '4' %}
                                    <td>运营公告</td>
                                {% elif obj.bulletinType == '1' %}
                                    <td>维护公告</td>
                                {% elif obj.bulletinType  == '2' %}
                                    <td>更新公告</td>
                                {% elif obj.bulletinType == '3' %}
                                    <td>活动公告</td>
                                {% else %}
                                    <td>未知公告</td>
                                {% endif %}
                                <td>{{ obj.exectime }}</td>
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
                                    <a href='#' onclick='del_message(this)' id={{ obj.id }} style="color:red">删除 </a>
                                    {#                                    <a href='#email_dialog' data-toggle='modal' name={{ obj.id }} style="color: #0D47A1">查看</a>#}
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
                                <a class="page-link" href="#" tabindex="-1" aria-disabled="true"
                                   onclick="click_page(this)" id="1">首页</a>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- /# card -->
            </div>
        </div>
        <!-- /# column -->
    </div>

{% endblock %}


{% block js %}
    <script type="text/javascript">


        var cell_map_to_idx = {
            id: 0,
            serverId: 1,
            title: 2,
            message: 3,
            bulletinType: 4,
            exectime: 5,
            is_confirm: 6,
        }
        var bulletin_type = {
            1: '维护公告',
            2: '更新公告',
            3: '活动公告',
        }
        var confirm_state = {
            0: '未执行',
            1: '已读取',
            2: '未确认',
            3: '处理失败',
            4: '禁用',
            5: '已删除',
        }

        function del_message(obj) {
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

        $(function () {

            var page = document.getElementById("page_info");
            var page_count = Math.ceil({{ total_row }}/ 10);
            setPageCookie({{ curr_page }}, page_count)

            for (var i = 1; i <= page_count;) {
                page.innerHTML += "<li class='page-item'><a class='page-link' href='#' id=" + i + " onclick='click_page(this)'>" + i + "</a></li>";
                i++;
            }
            page.innerHTML += "<li class='page-item'><a class='page-link' href='#' onclick='click_next(this)'>下一页</a></li>"
        })


        // 模态框 打开前
        $('#email_dialog').on('shown.bs.modal', function (event) {
            var rowId = event.relatedTarget.name
            var row = document.getElementById(rowId)


            let text7 = row.parentNode.parentNode.cells[cell_map_to_idx.createtime].innerText


            let title = row.parentNode.parentNode.cells[cell_map_to_idx.title].innerText
            document.getElementById("email_send_title").value = title;

            var context_value = row.parentNode.parentNode.cells[cell_map_to_idx.message].lastElementChild.innerHTML
            document.getElementById("email_send_context").value = context_value;

            {#var starttimes_value = row.parentNode.parentNode.cells[cell_map_to_idx.sendTimes].innerText#}
            {#document.getElementById("email_send_starttimes").value = starttimes_value;#}
            {##}
            {#var endtimes_value = row.parentNode.parentNode.cells[cell_map_to_idx.endTimes].innerText#}
            {#document.getElementById("email_send_endtimes").value = endtimes_value;#}


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
            var tbody = document.getElementById("message_tbody_list");
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
                text.innerText = obj.title

                text = NewRow.insertCell();
                text.innerHTML = "<textarea class='form-control' readonly='readonly' name='message' style='background-color: white'>" + obj.message + "</textarea>"

                text = NewRow.insertCell();
                text.innerText = bulletin_type[obj.bulletinType]

                text = NewRow.insertCell();
                text.innerText = obj.exectime

                text = NewRow.insertCell();
                text.innerText = confirm_state[obj.is_confirm] ?? '未知操作'


                // for (let key in obj) {
                //    if (obj.hasOwnProperty(key)) {
                //        text = NewRow.insertCell();
                //        text.innerText = obj[key].toString()
                //    }
                // }

                handle = NewRow.insertCell()
                handle.innerHTML = "<a href='#' onclick='del_message(this)' id=" + obj.id + " style='color:red'>删除 </a>"
                {#+"<a href='#email_dialog' data-toggle='modal' name=" + obj.id + " style='color: #0D47A1'>查看</a>"#}
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


        function read_email(obj) {
            dialog = document.getElementById("email_dialog")
            // dialog.
            alert(dialog)
        }


    </script>
{% endblock %}