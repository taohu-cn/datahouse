/**
 * Created by taohu on 2017/8/9.
 */

/**
 * @param data      需要渲染的数据
 * @param chart     图表生成对象
 * @param title     图表标题
 */
function renderChart(data, chart, title) {
    var option = {
        title: {
            text: title,
            subtext: '单位 Mb'
        },
        color: ['#3398DB'],
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        //legend: {},
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                magicType: {
                    type: ['line', 'bar']
                },
                dataView: {
                    show: true
                },
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            data: data.date,
            axisLabel: {
                alignWithLabel: true
                // interval: 0
                // rotate: 15
            }
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '备份大小',
                type: 'bar',
                barWidth: '40%',
                stack: '总量',
                data: data.size
            }
        ]
    };

    chart.hideLoading();
    chart.clear();
    chart.setOption(option);
}


function getData(id, memo) {
    /**
     * @param id    instance的id, 与表主键一致
     * @param memo  instance的描述信息, 自定义
     */
    var chart = echarts.init(document.getElementById(id), 'macarons');
    var url = '/api/data/size/' + id + '/';

    $.getJSON(
        url,
        function (data) {
            // console.log(data);
            renderChart(data, chart, memo)
        }
    );
}