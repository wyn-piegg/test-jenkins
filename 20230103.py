{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->
{% block head %}
    <link href="{% static 'plugins/daterangepicker-master/daterangepicker.css' %}" rel="stylesheet">
{% endblock %}

{% block content %}
    <!-- Modal -->
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
                                    <textarea class="form-control" placeholder="公告标题" id="context"
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
                                            style="vertical-align:top;outline:none;height: 50px;width: 100%;text-align: center">
                                        <option value="1">维护公告</option>
                                        <option value="2">更新公告</option>
                                        <option value="3">活动公告</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
                <button class="btn btn-primary btn-group-right" onclick="active_query()"
                        style="border: 1px solid ;width: 350px;margin-left: 30%;margin-right: auto">
                    <i class="ti-mouse-alt" href="uidModal">添加</i>
                </button>
            </div>
        </div>
    </div>


{% endblock %}

{% block js %}
    <script src="{% static 'plugins/daterangepicker-master/moment.min.js' %}"></script>
    <script src="{% static 'plugins/daterangepicker-master/daterangepicker.js' %}"></script>
    <script type="text/javascript">
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

        function active_query() {
            $.ajax({
                url: "", //url
                type: "post",//方法类型
                dataType: "JSON",//预期服务器返回的数据类型
                data: $('#message_info').serialize(),
                success: function (res) {
                    // 将后台返回的数据，更新到option中
                    // 使用刚指定的配置项和数据显示图表。
                    if (res.res) {
                        alert(res.message)
                    } else {

                    }
                }
            })
        }

        {#$('input[name="sendTime"]').on('apply.daterangepicker', function (ev, picker) {#}
            {#var endTime = new Date(picker.endDate.format('YYYY-MM-DD'))#}
        {#    var startTime = new Date(picker.startDate.format('YYYY-MM-DD'))#}
        {#    var nowTime = new Date()#}
        {#    if (startTime < nowTime) {#}
        {#        Y = nowTime.getFullYear() + '-';#}
        {#        M = (nowTime.getMonth() + 1 < 10 ? '0' + (nowTime.getMonth() + 1) : nowTime.getMonth() + 1) + '-';#}
        {#        D = nowTime.getDate() + ' ';#}
        {#        h = nowTime.getHours() + ':';#}
        {#        m = nowTime.getMinutes() + 10 + ':';#}
        {#        s = nowTime.getSeconds();#}
        {#        timeStr = Y + M + D + h + m + s#}
        {#        $('input[name="sendTime"]').data('daterangepicker').setStartDate(timeStr);#}
        {#    }#}
        //});
    </script>

{% endblock %}