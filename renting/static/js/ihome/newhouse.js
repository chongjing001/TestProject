function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    $.ajax({
        url:'/home/fac/',
        dataType:'json',
        type:'GET',
        success:function (data) {
            console.log(data)
            var i = 0
            var count = data.data1.length
            while(i<count){
                $('#area-id').append($('<option value="'+data.data1[i].id+'">'+data.data1[i].name+'</option>'))
                i++;
            }
            var j = 0
            var count1 = data.data.length
            while(j<count1){
                $('.house-facility-list').append($('<li><div class="checkbox"><label><input type="checkbox" name="facility" value="'+data.data[j].id+'">'+data.data[j].name+'</label></div></li>'))
                j++;
            }

        }

    })


    $("#form-house-info").submit(function(e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/home/newhouse/',
            dataType:'json',
            type:'POST',
            success:function (data) {
                console.log(data)
                $('#form-house-image').show()
                $('#form-house-info').hide()
                $('#house-id').val(data.id)

            },
            error:function (data) {
                alert('发布失败')
            }
        })

    });


    $("#form-house-image").submit(function(e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/home/add_himg/',
            dataType:'json',
            type:'POST',
            success:function (data) {
                console.log(data)
                // var num = data.count
                // var i = 0
                // while (i<num){
                //     $('.house-image-cons').append($('<img src="' + data.data[i] + '">'))
                //     i++;
                // }
                $('.house-image-cons').append($('<img src="' + data.data + '">'))
                // location.reload(true)
                // $('.popup i').html('发布成功，两秒后返回房源信息页面')
                // setTimeout(function(){
                //         // alert('我是延后2s调用的！')
                //
                //     },2000)


            },
            error:function (data) {
                alert('上传图片失败')
            }
        })

    });
})