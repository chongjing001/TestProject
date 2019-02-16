function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$(document).ready(function(){


    $("#form-auth").submit(function(e) {
        e.preventDefault();

        $("#real-name").focus(function() {
            $(".error-msg").hide();
        })
        $("#id-card").focus(function() {
            $(".error-msg").hide();
        })
        var id_name = $('#real-name').val()
        var id_card = $('#id-card').val()
        console.log(id_card,id_name)

        $.ajax({
            url: '/user/my_auth/',
            dataType: 'json',
            type: 'GET',
            data: {'id_name': id_name, 'id_card': id_card},
            success: function (data) {
                console.log(data)

                if (data.code == 200) {
                    showSuccessMsg()

                    // location.href='/user/index/'
                }
                else{
                    console.log('**************')
                    $('.error-msg').html(data.msg)
                    $('.error-msg').show()
                }
                // if (data.code == 1001) {
                //     $('.error-msg').html(data.msg)
                //     $('.error-msg').show()
                // }
                // if (data.code == 1002) {
                //     $('.error-msg').html(data.msg)
                //     $('.error-msg').show()
                // }

            }
        })
    })
})