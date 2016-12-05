$(".act-rule-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/sv/term/");
    }
});

$(".cls-rule-value").change(function(){
    console.log('rule value was changed');
    s_1 = $("#standin-rule-1").val();
    s_2 = $("#standin-rule-2").val();
    s_3 = $("#standin-rule-3").val();

    w_1 = $("#workday-rule-1").val();
    w_2 = $("#workday-rule-2").val();
    w_3 = $("#workday-rule-3").val();


    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/rule/",
          data: JSON.stringify({ group_id: 1,
           definition: {standin: [s_1, s_2, s_3], workday: [w_1, w_2, w_3]}})
        })
          .done(function( msg ) {
            console.log('rule value was saved');
          });

});
