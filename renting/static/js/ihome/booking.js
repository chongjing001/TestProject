function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24);
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var test = location.pathname
    var id = test.split('/')[3]
    $.ajax({
        url:'/home/my_detail/?id='+id,
        type:'GET',
        dataType:'json',
        success:function (data) {
            console.log(data)
            $('.h1').html(data.data.title)
            $('.s1').html(data.data.price)
            $('.house-info img').attr('src',data.data.images[0])


        },
        error:function (data) {
            alert('error')
        }
    });
   $(".submit-btn").on('click',function(e){
        e.preventDefault();
        var total = $('.order-amount').text().split('：')[1]
        var stime = $('#start-date').val()
        var endtime = $('#end-date').val()
        var h_title = $('.h1').html()
        var sd = new Date(stime);
        var ed = new Date(endtime);
        days = (ed - sd)/(1000*3600*24);
        console.log(sd, ed, days)
        var h_id = test.split('/')[3]
       console.log(total,stime,endtime,h_title,h_id)
        $.ajax({
            url: '/order/stay/',
            dataType: 'json',
            type: 'POST',
            data:{'t':total,'st':stime,'et':endtime,'tit':h_title,'h_id':h_id,'d':days},
            success:function (data) {
                console.log(data)
                location.href = '/order/orders/'
            },
            error:function (data) {
                alert('error')
            }
        })


    })

})
