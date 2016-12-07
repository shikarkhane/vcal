$(".act-term-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/sv/template/done/");
    }
});


$("#term-save").click(function(){
    name = $("#term-name").val();
    start = $("#term-start-date").val();
    end = $("#term-end-date").val();
    f_1 = $("#term-family-1").val();
    f_2 = $("#term-family-2").val();
    f_3 = $("#term-family-3").val();


    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/term/",
          data: JSON.stringify({ group_id: 1,
          term_name: name, start_date: start, end_date: end,
           family_spread: {kid_1: f_1, kid_2: f_2, kid_3: f_3}})
        })
          .done(function( msg ) {
            console.log('term was saved');
          });

});
