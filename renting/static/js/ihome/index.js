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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    // var url = "/search.html?";
    // url += ("aid=" + $(th).attr("area-id"));
    // url += "&";
    // var areaName = $(th).attr("area-name");
    // if (undefined == areaName) areaName="";
    // url += ("aname=" + areaName);
    // url += "&";
    // url += ("sd=" + $(th).attr("start-date"));
    // url += "&";
    // url += ("ed=" + $(th).attr("end-date"));
    // console.log(url)
    // location.href = url;


    var a_id = $(th).attr('area-id')
    // var a_name = $(th).attr('area-name')
    var st_date = $(th).attr('start-date')
    var end_date = $(th).attr('end-date')
    location.href = '/home/search/?a_id='+a_id+'&st_date='+st_date+'&end_date='+end_date+''

    // $.ajax({
    //     url:'/home/s_info/',
    //     dataType:'json',
    //     type:'GET',
    //     data:{'a_id':a_id,'a_name':a_name,'st_date':st_date,'end_date':end_date},
    //     success:function (data) {
    //         console.log(data)
    //         location.href='/home/search/'
    //     },
    //     error:function (data) {
    //         alert('error')
    //     }
    // })
}

$(document).ready(function(){
    $(".top-bar>.register-login").show();
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationClickable: true
    }); 
    $(".area-list a").click(function(e){
        $("#area-btn").html($(this).html());
        $(".search-btn").attr("area-id", $(this).attr("area-id"));
        $(".search-btn").attr("area-name", $(this).html());
        $("#area-modal").modal("hide");
    });
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });

    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function (data) {
            console.log(data)
            if(data.flag){
                alert('退出成功')
            }
            if(data.data.name){
                $('#reg').html(data.data.name)
                $('.register-login').hide()
                $('.user-info').show()

            }
        },
        error:function (data) {
            alert('error')
        }


    });

    $.ajax({
        url: '/home/index_info/',
        dataType: 'json',
        type:'GET',
        success:function (data) {
            console.log(data)
            var i = 0
            var count = data.count
            if(count>5){
                count = 5
            }

            while(i<count){

                 $('.swiper-wrapper').append($('<div class="swiper-slide"><a href="/home/detail/'+data.data[i].id+'"><img src="'+data.data[i].image+'"></a>' +
                '<div class="slide-title">'+data.data[i].title+'</div></div>'))
                i++;
            }


            // 轮播图
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationClickable: true
            });
        },
        error:function (data) {
            alert('error')
        }
    });
    $.ajax({
        url:'/home/fac/',
        dataType:'json',
        type:'GET',
        success:function (data) {
            console.log(data)
            var i = 0
            var count = data.data1.length
            while (i<count){
                $('.area-list').append($('<a href="#" area-id="'+data.data1[i].id+'">'+data.data1[i].name+'</a>'))
                i++;
            }
            $(".area-list a").click(function(e){
            $("#area-btn").html($(this).html());
            $(".search-btn").attr("area-id", $(this).attr("area-id"));
            $(".search-btn").attr("area-name", $(this).html());
            $("#area-modal").modal("hide");
            });


        },
        error:function (data) {
            alert('error')
        }

    })




})