function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // var mySwiper = new Swiper ('.swiper-container', {
    //     loop: true,
    //     autoplay: 2000,
    //     autoplayDisableOnInteraction: false,
    //     pagination: '.swiper-pagination',
    //     paginationType: 'fraction'
    // });




    var test = window.location.pathname;
    console.log(test)
    var id = test.split('/')[3]
    console.log(id)

    $.ajax({
        url: '/home/my_detail/?id='+id,
        type:'GET',
        dataType:'json',
        success:function (data) {

            if(data.flag1&&data.flag){
                $('.book-house').html('需登录后方可预定，点我去登陆')
                $('.book-house').attr('href','/user/login/')
                $('.book-house').show()
            }

            if(data.flag&&!data.flag1){
                $('.book-house').attr('href', '/order/booking/'+data.data.id+'/')
                $(".book-house").show();
            }
            if(!data.flag){
                $('.book-house').html('欢迎主人，点我去订单页面')
                $('.book-house').attr('href','/order/lorders/')
                $('.book-house').show()
            }

            console.log(data)
            $('.house-title').html(data.data.title);
            $('.landlord-pic img').attr('src','/static/media/'+data.data.user_avatar);
            $('.landlord-name span').html(data.data.user_name);
            $('.house-info-list .l1').html(data.data.address);
            $('.icon-text .h1').html('出租'+data.data.room_count+'间');
            $('.icon-text .p1').html('房屋面积：'+data.data.acreage+'平米');
            $('.icon-text .p2').html('房屋户型：'+data.data.unit);
            $('.icon-text .h2').html('宜住'+data.data.capacity);
            $('.icon-text .p3').html(data.data.beds);
            $('.s1').html(data.data.deposit);
            $('.s2').html(data.data.min_days);
            $('.s3').html(data.data.max_days);
            $('.s4').html(data.data.price);
            var i = 0;
            var fa_num = data.data.facilities.length;
            while (i<fa_num){
                $('.house-facility-list').append($('<li><span class="'+data.data.facilities[i].css+'"></span>'+data.data.facilities[i].name+'</li>'));
                i++;
            }

            var j = 0;
            var num = data.data.images.length;
            console.log(num)

            while(j<num){
                $('#ul_img').append($('<li class="swiper-slide"><img src="'+data.data.images[j]+'"></li>'));
                // $('.swiper-slide').attr('src',data.data.images[i]);
                j++;
            }
             var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });

            // $('.book-house').attr('href', '/order/booking/?house_id='+data.data.id)






        },
        error:function (data) {
            alert('error')
        }

    })
})