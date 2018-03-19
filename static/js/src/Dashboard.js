/**
 * Created by taohu on 2017/8/30.
 */


function getInstance() {
    /**
     * 获取所有instance信息, 包括 id ip port db_usage
     */
    var CD = $("#content_dashboard");

    var url = '/api/data/instances/';
    $.getJSON(
        url,
        function (data) {
            $.each(data, function (index, ele) {
                var html = '<div id=' + ele.id + ' style="height: 350px; margin: 80px">' + index + '</div>';
                CD.append(html);
                console.log(html);
                var memo = ele.db_usage + ' (' + ele.host + ':' + ele.port + ')';
                getData(ele.id, memo);
            })
        }
    )
}

$(document).ready(function () {
    getInstance();
});