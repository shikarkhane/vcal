$( document ).ready(function() {
    if ($.cookie("usertype")){
        $(".act-username")[0].textContent=$.cookie("usertype");
    }
    else{
        $(".act-username").closest('.ui-btn').hide();
    }
    if( $.cookie("show_work_step") == 1){
        $(".act-work-step").show();
        $(".clsnextstep").closest('.ui-btn').show();
        update_work_step();
    }
    else{
        $(".act-work-step").hide();
        $(".clsnextstep").closest('.ui-btn').hide();
    }

});
function update_work_step(){
    var p = window.location.pathname.replace('sv', '').replace('template', '').replace(/\//g, '');
    var el = $(".step-" + p);
    if (el.length > 0){
        el.prevAll().removeClass('todo').addClass('done');
        if ( p == 'done'){
            el.removeClass('todo').addClass('done');
        }
    }
    else{
        // user has escaped the work-step flow, dont show work -step
        $(".act-work-step").hide();
    }
};
$(".act-home").click(function(){
    window.location.replace("/sv/dashboard/"+$.cookie("usertype")+'/');
});
$(".act-sign-up").click(function(){
    window.location.replace("/sv/");
});

$(".act-is-admin").click(function(){
    $.cookie("usertype", "admin");
    window.location.replace("/sv/dashboard/"+$.cookie("usertype")+'/');
});
$(".act-is-user").click(function(){
    $.cookie("usertype", "user");
    window.location.replace("/sv/dashboard/"+$.cookie("usertype") +'/');
});

$(".act-log-in").click(function(){
    window.location.replace("/sv/");
});
$(".act-summon").click(function(){
    window.location.replace("/sv/template/summon/");
});
$(".act-work-day").click(function(){
    window.location.replace("/sv/workday/");
});
$(".act-term").click(function(){
    window.location.replace("/sv/term/");
});
$(".act-show-ups").click(function(){
    window.location.replace("/sv/template/show-ups/");
});
$(".act-invite").click(function(){
    window.location.replace("/sv/invite/");
});
$(".act-members").click(function(){
    window.location.replace("/sv/member/");
});
$(".act-switch-day").click(function(){
    window.location.replace("/sv/switchday/");
});

$(".act-children").click(function(){
    window.location.replace("/sv/template/children/");
});
$(".act-work-sign-up").click(function(){
    window.location.replace("/sv/template/work-sign-up/");
});
$(".act-rule").click(function(){
    window.location.replace("/sv/rule/");
});
$(".act-username").click(function(){
    $.cookie("show_work_step", 0, { path: '/' });
    window.location.replace("/sv/");
});
$(".act-create-group").click(function(){
    window.location.replace("/sv/group/");
});

$(".act-done-nextstep").click(function(){
    $.cookie("show_work_step", 0, { path: '/' });
    window.location.replace("/sv/dashboard/"+$.cookie("usertype")+'/');
});