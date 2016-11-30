$(".act-term-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/sv/template/done/");
    }
});
