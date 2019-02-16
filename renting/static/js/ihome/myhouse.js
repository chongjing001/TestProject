$(document).ready(function(){

    // 用户信息
    $.ajax({
        url:'/user/user_info/',
        dataType:'json',
        data:'GET',
        success:function (data) {
            console.log(data)
            if(data.data1.id_card){
                $(".auth-warn").hide();
            }
            else{
                $(".auth-warn").show();
                $('#houses-list').hide();
            }
        },
        error:function (data) {
            alert('error')
        }
    });

//    房屋信息
    $.ajax({
        url: '/home/house_info/',
        dataType: 'json',
        type:'GET',
        success:function (data) {
            console.log(data)
            if(data.count==0){
                $('#houses-list').append($('<div>当前还没有房源哦</div>'))
            }
            else{
                console.log(data.data[0].title)
                var count = data.count;
                var i = 0
                while (i<count){
                    var li = $('<li>' +
                        '<a id="l_de" href="/home/detail/'+data.data[i].id+'/">' +
                            '<div class="house-title">' +
                                '<h3>'+'房屋ID：'+data.data[i].id+'——'+data.data[i].title+'</h3></div>' +
                            '<div class="house-content">' +
                                '<img src="'+data.data[i].image+'">' +
                                '<div class="house-text">' +
                                    '<ul>' +
                                        '<li id="l_addr">'+'位于：'+data.data[i].area+'</li>' +
                                        '<li id="l_price">'+'价格：'+'￥'+data.data[i].price+'/晚'+'</li>' +
                                        '<li id="l_uptime">'+'发布时间：'+data.data[i].create_time+'</li>' +
                                    '</ul>' +
                                '</div>' +
                            '</div>' +
                        '</a>' +
                        '</li>')

                    $('#houses-list').append(li);
                    i++;
                }

            }

            // $('house-title h3').html('房屋ID:'+data.id+'——'+data.title)
        },
        error:function (data) {
            alert('error')
        }
    })


})