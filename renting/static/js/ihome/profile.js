function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

    $("#form-avatar").submit(function(e){


        $(this).ajaxSubmit({
            url:'/user/profile/',
            type:'post',
            dataType:'json',
            success:function (data) {
                console.log(data)
                if(data.code==200){
                    $('#user-avatar').attr('src','/static/media/'+ data.data.avatar)
                    location.href='/user/index/'
                }
            },
            error:function (data) {
                alert('error')
            }

        })

    })

    $("#form-name").submit(function(e){
        $(this).ajaxSubmit({
            url:'/user/profile/',
            type:'post',
            dataType:'json',
            success:function (data) {
                console.log(data)
                if(data.code==200){
                    $('#username').html(data.data.name)
                    location.href='/user/index/'
                }
            },
            error:function (data) {
                alert('error')
            }
        })

    })


})