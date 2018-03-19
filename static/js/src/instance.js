/**
 * Created by taohu on 2017/10/23.
 */

function getInstance() {
    var CD = $("#instance_dashboard");
    var url = '/api/data/instances/?pro_id=' + $('#table').data('pro_id');

    $.getJSON(
        url,
        function (data) {
            // console.log(data);
            $.each(data, function (index, ele) {
                var html = '<div id=' + ele.id + ' style="height: 350px; margin: 80px">' + index + '</div>';
                CD.append(html);
                var memo = ele.db_usage + ' (' + ele.host + ':' + ele.port + ')';
                getData(ele.id, memo);
            })
        }
    )
}

$(document).ready(function () {
    getInstance();
});