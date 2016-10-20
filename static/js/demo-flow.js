window.usertype = 'user'
$(".act-home").click(function(){
    window.location.replace("/dashboard/"+window.usertype+'/');
});
$(".act-sign-up").click(function(){
    window.location.replace("/");
});

$(".act-is-admin").click(function(){
    window.usertype = 'admin';
    window.location.replace("/dashboard/"+window.usertype+'/');
});
$(".act-is-user").click(function(){
    window.usertype = 'user';
    window.location.replace("/dashboard/"+window.usertype+'/');
});

$(".act-log-in").click(function(){
    window.location.replace("/dashboard/"+window.usertype+'/');
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

