function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url:'/user/user_info/',
        dataType:'json',
        type:'get',
        success:function (data) {
            console.log(data)
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.phone)
            $('#user-avatar').attr('src','/static/media/'+data.data.avatar)
        }
    })
})