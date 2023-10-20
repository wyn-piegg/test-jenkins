{% extends 'layout_left.html' %}
{% load static %} <!-- 必写,Django根据seting自动查找当前App静态文件 -->

{% block head %}
    <link href="{% static '/layui/css/layui.css' %}" rel="stylesheet">
{% endblock %}


{% block content %}
    <div class="layui-form">
        <div class="layui-form-item">
            <div class="layui-inline">
                <label class="layui-form-label">范围</label>
                <div class="layui-input-inline">
                    <input type="text" class="layui-input" id="test16" placeholder="开始 到 结束">
                </div>
                <button class="layui-btn" id="select_btn" lay-event="select_btn"><i class="layui-icon">&#xe615;</i>查询
                </button>
            </div>
        </div>

    </div>

    <!-- column -->
    <div class="col-lg-12">
        <div class="card">
            <div class="card-body" style="height: 500px">
                <h4 class="card-title">新增用户</h4>
                <div id="main" style="width: 100%; height: 100%"></div>
            </div>
        </div>
    </div>

{% endblock %}

{% block js %}
    <script src="{% static 'js/echarts.min.js' %}"></script>
    <script src="{% static 'layui/layui.js' %}" charset="utf-8"></script>

    <script type="text/javascript">
        var dom = document.getElementById('main');
        var myChart = echarts.init(dom, null, {
            renderer: 'canvas',
            useDirtyRect: false
        });
        var app = {};

        var option;

        option = {
            title: {
                text: 'Stacked Line'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '新增人数',
                    type: 'line',
                    stack: 'Total',
                    data: [120, 132, 101, 134, 90, 230, 210]
                },
            ]
        };

        if (option && typeof option === 'object') {
            myChart.setOption(option);
        }

        window.addEventListener('resize', myChart.resize);

        layui.use(['form', 'table', "laydate", 'layer'], function () {
            var table = layui.table;
            var form = layui.form;
            var layer = layui.layer;
            var laydate = layui.laydate;
            var $ = layui.$;

            laydate.render({
                elem: '#test16'
                , type: 'datetime'
                , range: '-'
                , format: 'yyyy/M/d H:m:s'
            });

            $("#select_btn").on('click', function () {

                if ($('#codeInfo').val() === '') {
                    layui.use('layer', function () {
                        var layer = layui.layer;
                        layer.open({
                            title: '提示消息',
                            content: '查询条件不存在！'
                        });
                    });
                }

            });

    </script>


    {#<script type="text/javascript">#}
    {##}
    {#    $(function () {#}
    {#        $('input[name="datetimes"]').daterangepicker({#}
    {#            timePicker: true,//可选中时分 默认false#}
    {#            timePicker24Hour: true,//设置小时为24小时制 默认false#}
    {#            //autoUpdateInput:false,//1.当设置为false的时候,不给与默认值(当前时间)2.选择时间时,失去鼠标焦点,不会给与默认值 默认true#}
    {#            startDate: moment().startOf('hour'),#}
    {#            endDate: moment().startOf('hour').add(32, 'hour'),#}
    {#            ranges: {#}
    {#                '今天': [moment().startOf('days'), moment()],#}
    {#                '昨天': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],#}
    {#                '近7天': [moment().subtract(7, 'days'), moment()],#}
    {#                '这个月': [moment().startOf('month'), moment().endOf('month')],#}
    {#                '上个月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]#}
    {#            },#}
    {#            locale: {#}
    {#                format: 'YYYY-MM-DD HH:mm',#}
    {#                separator: "-",#}
    {#                customRangeLabel: "自定义",#}
    {#                applyLabel: "确定",#}
    {#                cancelLabel: "取消",#}
    {#                fromLabel: "起始时间",#}
    {#                toLabel: "结束时间",#}
    {#                weekLabel: "w",#}
    {#                daysOfWeek: ["日", "一", "二", "三", "四", "五", "六"],#}
    {#                monthNames: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],#}
    {#            }#}
    {#        });#}
    {##}
    {#        initCharts();#}
    {#    })#}
    {##}
    {#    function active_query() {#}
    {#        $.ajax({#}
    {#            url: "/operate/add/", //url#}
    {#            type: "post",//方法类型#}
    {#            dataType: "JSON",//预期服务器返回的数据类型#}
    {#            data: $('#query_from').serialize(),#}
    {#            success: function (res) {#}
    {#                // 将后台返回的数据，更新到option中#}
    {#                // 使用刚指定的配置项和数据显示图表。#}
    {#                if (res.status) {#}
    {#                    initCharts(res.data)#}
    {#                }#}
    {#                myChart.setOption(option);#}
    {#            }#}
    {#        })#}
    {#    }#}
    {##}
    {#    function initCharts(res) {#}
    {#        // 基于准备好的dom，初始化echarts实例#}
    {#        var myChart = echarts.init(document.getElementById("main"));#}
    {##}
    {#        // 指定图表的配置项和数据#}
    {#        var option = {#}
    {#            title: {#}
    {#                // text: 'ECharts 入门示例'#}
    {#            },#}
    {#            tooltip: {},#}
    {#            legend: {#}
    {#                data: res.legend#}
    {#            },#}
    {#            xAxis: { //#}
    {#                data: res.x_axis#}
    {#            },#}
    {#            yAxis: {},#}
    {#            series: [#}
    {#                {#}
    {#                    name: '活跃用户',#}
    {#                    type: 'line',#}
    {#                    smooth: true,#}
    {#                    data: res.series_list,#}
    {#                },#}
    {#            ]#}
    {#        };#}
    {##}
    {#option.legend.data = res.legend#}
    {#option.xAxis.data = res.x_axis#}
    {#option.series = res.series_list#}
    {#        #}
    {#        myChart.setOption(option);#}
    {#    }#}
    {#    $('input[name="datetimes"]').on('apply.daterangepicker', function (ev, picker) {#}
    {#            var endTime = new Date(picker.endDate.format('YYYY-MM-DD'))#}
    {#            var nowTime = new Date()#}
    {#            if (endTime > nowTime) {#}
    {#                Y = nowTime.getFullYear() + '-';#}
    {#                M = (nowTime.getMonth() + 1 < 10 ? '0' + (nowTime.getMonth() + 1) : nowTime.getMonth() + 1) + '-';#}
    {#                D = nowTime.getDate() + ' ';#}
    {#                h = nowTime.getHours() + ':';#}
    {#                m = nowTime.getMinutes() + ':';#}
    {#                s = nowTime.getSeconds();#}
    {#                timeStr = Y+M+D+h+m+s#}
    {#                $('input[name="datetimes"]').data('daterangepicker').setEndDate(timeStr);#}
    {#            }#}
    {#        });#}
    {##}
    {#</script>#}


    la


{% endblock %}