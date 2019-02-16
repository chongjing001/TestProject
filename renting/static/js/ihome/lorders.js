//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // $(".order-accept").on("click", function(){
    //     var orderId = $(this).parents("li").attr("order-id");
    //     $(".modal-accept").attr("order-id", orderId);
    // });
    // $(".order-reject").on("click", function(){
    //     var orderId = $(this).parents("li").attr("order-id");
    //     $(".modal-reject").attr("order-id", orderId);
    // });

    //  onclick="acc(this)"
    // function acc(evt) {
    //     console.log(evt)
    // }
    //
    // function rej(evt) {
    //     console.log(evt)
    // }

    $.ajax({
        url:'/order/other_info/',
        dataType:'json',
        type:'GET',
        success:function (data) {
            console.log(data)
            var i = 0;
            var count = data.data.length
            if(count==0){
                $('.orders-list').append($('<div class="is_null">空空如也</div>'))
            }
            while (i<count){
                $('.orders-list').append($(
                    '<li id="'+data.data[i].order_id+'">' +
                        '<div class="order-title">' +
                            '<h3>订单编号：LoveIn2019'+data.data[i].order_id+'</h3>' +
                            '<div class="fr order-operate" id="'+data.data[i].order_id+'">' +
                                '<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal" order_id="'+data.data[i].order_id+'">接单</button>' +
                                '<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal" order_id="'+data.data[i].order_id+'">拒单</button>' +
                            '</div>' +
                    '   </div>' +
                        '<div class="order-content">' +
                            '<img src="'+data.data[i].image+'">' +
                            '<div class="order-text">' +
                                '<h3>'+data.data[i].house_title+'</h3>' +
                                '<ul>' +
                                    '<li>创建时间：'+data.data[i].create_date+'</li>' +
                                    '<li>入住时间：'+data.data[i].begin_date+'</li>' +
                                    '<li>离开日期：'+data.data[i].end_date+'</li>' +
                                    '<li>合计金额：'+data.data[i].amount+'元(共'+data.data[i].days+'晚)</li>' +
                                    '<li class="">订单状态：' +
                                        '<span class="d1">'+data.data[i].status+'</span>' +
                                    '</li>' +
                                    '<li class="w1">拒单原因：'+data.data[i].comment+'</li>' +
                                '</ul>' +
                            '</div>' +
                        '</div>' +
                    '</li>'))

                var order_s = $('#'+data.data[i].order_id+' .d1').html()
                var eva = $('#'+data.data[i].order_id+' .w1').html().split('：')[1]
                if(order_s=='WAIT_ACCEPT'){
                    $('#'+data.data[i].order_id+' .d1').html('待接单')
                }
                else{
                    $('.order-operate').hide()
                }
                if(order_s=='WAIT_PAYMENT'){
                    $('#'+data.data[i].order_id+' .d1').html('待支付')
                }
                if(order_s=='PAID'){
                    $('#'+data.data[i].order_id+' .d1').html('已支付')
                }
                if(order_s=='WAIT_COMMENT'){
                    $('#'+data.data[i].order_id+' .d1').html('待评价')
                }
                if(order_s=='COMPLETE'){
                    $('#'+data.data[i].order_id+' .d1').html('已完成')
                }
                if(order_s=='CANCELED'){
                    $('#'+data.data[i].order_id+' .d1').html('已取消')
                }
                if(order_s=='REJECTED'){
                    $('#'+data.data[i].order_id+' .d1').html('已拒单')
                }
                if(eva=='null'){
                    $('#'+data.data[i].order_id+' .w1').hide()
                }


                i++;
            } // while循环



            $(".order-accept").on("click", function(){
                var orderId = $(this).attr("order_id");
                console.log(orderId)
                $(".modal-accept").attr("order_id", orderId);
            });

            $(".order-reject").on("click", function(){
                var orderId = $(this).attr("order_id");
                console.log(orderId)
                $(".modal-reject").attr("order_id", orderId);
            });

            $('.modal-accept').click(function(){

                var order_id = $(".modal-accept").attr("order_id")
                var status = 'WAIT_PAYMENT'
                $.ajax({
                    url:'/order/order/',
                    data:{'order_id': order_id, 'status': status},
                    dataType:'json',
                    type:'PATCH',
                    success:function(data){
                        location.reload()
                    },
                    error:function(data){
                        alert('请求失败')
                    }

                })
            })

            $('.modal-reject').click(function(){
                var order_id = $('.modal-reject').attr('order_id')
                var status = 'REJECTED'
                var comment = $('#reject-reason').val()

                $.ajax({
                    url:'/order/order/',
                    type:'PATCH',
                    dataType:'json',
                    data:{'order_id': order_id, 'status': status, 'comment':comment},
                    success:function(data){
                        location.reload()
                    },
                    error:function(data){
                        alert('请求失败')
                    }
                })

            })


        },
        error:function (data) {
            alert('error')
        }
    })
});