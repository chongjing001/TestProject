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
    // $(".order-comment").on("click", function(){
    //     var orderId = $(this).parents("li").attr("order-id");
    //     $(".modal-comment").attr("order-id", orderId);
    // });




    $.ajax({
        url:'/order/order_info/',
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
                            '<div class="fr order-operate">' +
                                '<button type="button" class="btn btn-success order-comment"  data-toggle="modal" data-target="#comment-modal">发表评价</button>' +
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
                                    '<li class="j1">拒单原因：</li>' +
                                '</ul>' +
                            '</div>' +
                        '</div>' +
                    '</li>'))



            //
                 $('.order-operate button').hide()
                var order_s = $('#'+data.data[i].order_id+' .d1').html()
                var eva = $('#'+data.data[i].order_id+' .w1').html().split('：')[1]
                var reason = $('#'+data.data[i].order_id+' .j1').html().split('：')[1]
                console.log(order_s,eva,reason)
                if(order_s=='WAIT_ACCEPT'){
                    $('#'+data.data[i].order_id+' .d1').html('待接单')
                }
                if(order_s=='WAIT_PAYMENT'){
                    $('#'+data.data[i].order_id+' .d1').html('待支付')
                    $('#'+data.data[i].order_id+' .order-operate').append($('<input  class="btn-on"  data-toggle="modal" data-target="#accept-modal" type="button" order_id="'+data.data[i].order_id+'" value="去付款">'))
                    // $('#'+data.data[i].order_id+' .order-operate .btn').html('取消订单')

                    $('#'+data.data[i].order_id+' .order-operate').append($('<input  class="btn-off"  data-toggle="modal" data-target="#reject-modal" type="button" order_id="'+data.data[i].order_id+'" value="取消订单">'))
                    // $('#'+data.data[i].order_id+' .order-operate button').show()

                }
                if(order_s=='PAID'){
                    $('#'+data.data[i].order_id+' .d1').html('已支付')

                }
                if(order_s=='WAIT_COMMENT'){
                    $('#'+data.data[i].order_id+' .d1').html('待评价')
                    $('.order-operate button').show()
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
                if(!reason){
                    $('#'+data.data[i].order_id+' .j1').hide()
                }


                i++;
            } // while 循环

            $(".btn-off").on("click", function(){
                var orderId = $(this).attr("order_id");
                console.log('house_id:',orderId)
                $(".modal-accept").attr("order_id", orderId);
            });

            $(".btn-on").on("click", function(){
                var orderId = $(this).attr("order_id");
                console.log('house_id:',orderId)
                $(".modal-reject").attr("order_id", orderId);
            });

            $('.modal-accept').click(function(){

                var order_id = $(".modal-accept").attr("order_id")
                console.log('id:',order_id)
                var status = 'PAID'
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
                var status = 'CANCELED'
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

        },  //success
        error:function (data) {
            alert('error')
        }
    })
});