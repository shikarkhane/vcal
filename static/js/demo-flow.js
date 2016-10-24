$( document ).ready(function() {
    if ($.cookie("usertype")){
        $(".act-username")[0].textContent=$.cookie("usertype");
    }
    else{
        $(".act-username").closest('.ui-btn').hide();
    }
    if( $.cookie("show_work_step") == 1){
        $(".act-work-step").show();
    }
    else{
        $(".act-work-step").hide();
    }
});
$(".act-home").click(function(){
    window.location.replace("/dashboard/"+$.cookie("usertype")+'/');
});
$(".act-sign-up").click(function(){
    window.location.replace("/");
});

$(".act-is-admin").click(function(){
    $.cookie("usertype", "admin");
    window.location.replace("/dashboard/"+$.cookie("usertype")+'/');
});
$(".act-is-user").click(function(){
    $.cookie("usertype", "user");
    window.location.replace("/dashboard/"+$.cookie("usertype") +'/');
});

$(".act-log-in").click(function(){
    window.location.replace("/");
});
$(".act-summon").click(function(){
    window.location.replace("/template/summon/");
});
$(".act-work-day").click(function(){
    window.location.replace("/template/work-day/");
});
$(".act-term").click(function(){
    window.location.replace("/template/term/");
});
$(".act-show-ups").click(function(){
    window.location.replace("/template/show-ups/");
});
$(".act-invite").click(function(){
    window.location.replace("/template/invite/");
});
$(".act-members").click(function(){
    window.location.replace("/template/members/");
});
$(".act-children").click(function(){
    window.location.replace("/template/children/");
});
$(".act-work-sign-up").click(function(){
    window.location.replace("/template/work-sign-up/");
});
$(".act-rule").click(function(){
    window.location.replace("/template/rule/");
});
$(".act-username").click(function(){
    window.location.replace("/dashboard/"+$.cookie("usertype")+'/');
});
$(".act-create-group").click(function(){
    window.location.replace("/template/group/");
});
$(".act-save-group").click(function(){
    $.cookie("show_work_step", 1);
    window.location.replace("/template/invite/");
});
$(".act-send-invites").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/template/work-day/");
    }
    window.location.replace("/template/members/");
});
$(".act-workday-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/template/rule/");
    }
});
$(".act-term-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/template/done/");
    }
});