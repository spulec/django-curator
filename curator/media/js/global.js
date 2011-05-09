WIDGET_SIZE_FACTOR = .97
WIDGET_FULLSCREEN_HEIGHT = .9
WIDGET_FULLSCREEN_WIDTH = .98

var chart_data = {};
var chart_options = {};
var widget_urls = {};
var widget_labels = {};

function redraw_chart(widget_id) {
    $.plot($("#chart_div" + widget_id), chart_data[widget_id], chart_options[widget_id]);
}

function show_tooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
            'font-size': '16px',
            border: '1px solid #fdd',
            padding: '2px',
            'background-color': '#fee',
            opacity: 0.80,
            'z-index': 1000,
        }).appendTo("body").fadeIn(200);
}

function load_chart(widget_id) {
    //$("#data_loading_img" + widget_id).show();
    var data_list = [
            {data: [], color: "silver"},
            {data: [], label: widget_labels[widget_id], color: "blue"},
        ];
    
    var options = {
        xaxis: { mode: "time" },
        yaxis: { min: 0 },
        legend: {
            backgroundOpacity: 0,
            position: "nw",
        },
        grid: {
            hoverable: true
        },
        series: {
            lines: { show: true },
            //points: { show: true },
        },
    }
    
    chart_data[widget_id] = data_list;
    chart_options[widget_id] = options;
    redraw_chart(widget_id);
    reload_chart_data(widget_id);
}

function reload_chart_data(widget_id) {
    $("#data_loading_img" + widget_id).show();
    
    $.ajax({
        method: "GET",
        dataType: 'json',
        url: widget_urls[widget_id],
        success: function(json_data) {
            console.log("success-data-ajax: " + json_data['data_points'].length);
            
            data_list = chart_data[widget_id];
            convert_json_times(json_data['prev_data_points'], data_list[0]);
            convert_json_times(json_data['data_points'], data_list[1]);
            
            options = chart_options[widget_id];
            options.xaxis = {
                mode: "time",
                minTickSize: [1, json_data['time_intervals']],
            }
            options.offset = json_data['prev_time_offset'] * 1000;
            
            height = json_data['height'];
            width = json_data['width'];
            $("#chart_div" + widget_id).height(height - 30);
            $("#chart_div" + widget_id).width(width - 30);
            
            redraw_chart(widget_id);
            $("#data_loading_img" + widget_id).hide();
        }
    });
}

function convert_json_times(json_times, series_data) {
    series_data.data = [];
    
    $.each(json_times, function(index, value) {
        value[0] = new Date(value[0] * 1000).getTime();
        series_data.data.push(value);
    });
}

jQuery(document).ready(function($) {

    var previous_point_index = null;
    var previous_point_series = null;
    $(".chart_div").bind("plothover", function (event, pos, item) {
        if (item) {
            if (previous_point_index != item.dataIndex || previous_point_series != item.seriesIndex) {
                previous_point_index = item.dataIndex;
                previous_point_series = item.seriesIndex;
            
                $("#tooltip").remove();
                if (item.seriesIndex == 0){
                    var datetime = new Date(item.datapoint[0] - chart_options[$(this).data('id')].offset);
                }else {
                    var datetime = new Date(item.datapoint[0]);
                }
                var value = item.datapoint[1];
            
                show_tooltip(item.pageX, item.pageY, datetime.toUTCString() + " = " + value);
            }
        } else {
            $("#tooltip").remove();
            previousPoint = null;
        }
    });
    
    $(".edit_btn").button({
        text: false,
        icons: {
            primary: "ui-icon-minusthick"
        }
    });
    
    $(".edit_btn").live("click", function() {
        window.open($(this).data('url'),'_newtab');
    });
    
    $(".reload_btn").button({
        text: false,
        icons: {
            primary: "ui-icon-arrowrefresh-1-e"
        }
    });
    
    $(".reload_btn").live("click", function() {
        reload_chart_data($(this).data('id'));
        //load_chart($(this).data('id'));
    });
    
    for(var widget_id in chart_data) {
        setInterval("load_chart(" + widget_id + ")", 60000);
    }

});
