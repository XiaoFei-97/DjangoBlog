//滚动事件
$(function(){
    $(window).scroll(function(){
        var top=$(window).scrollTop();
        var navbar = $(".navbar-fixed-top");

        if(top==0){
            $(".navbar-fixed-top").removeClass("navbar-down");
        }else{
            $(".navbar-fixed-top").addClass("navbar-down");
        }

        if(top>350){
            $("#scrolltop").fadeIn();
        }else{
            $("#scrolltop").fadeOut();
        }
    });

    //点击返回头部效果
    $("#scrolltop").click(function(){
        $("html,body").animate({
            scrollTop:0});
    });
});

//登录注册按钮
$(function () {
    $("#login_button").click(function () {
        $('#login_modal').modal('show');
    });
    // 注册按钮
    $("#register_button").click(function () {
        $('#register_modal').modal('show');
    });
    // 找回密码
    $("#forgot_password_button").click(function () {
        $('#login_modal').modal('hide');
        $('#forgot_password_modal').modal('show');
    });
});

// 检查搜索框
function check() {
    var key = $("#key").val();

    if(key == null || key == ""){
        // alert("搜索内容不能为空！");
        window.location.href = '/blog';
        return false;
    }
    return true;
}

// 轮播图操作
$(function(){
    // 初始化轮播
    $("#myCarousel").carousel('cycle');
    $('#myCarousel').carousel({
        interval: 3000
    });
});