
$(".act-workday-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/sv/rule/");
    }
});

$("#create-workday-save").click(function(){
    work_date = $("#create-workday-date").val();
    from_time = $("#create-workday-fromtime").val();
    to_time = $("#create-workday-totime").val();
    is_half_day = $("#create-workday-halfday").val();

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/workday/",
          data: JSON.stringify({ created_by_id: 1, group_id: 1, work_date: work_date,
          from_time: from_time, to_time: to_time, standin_user_id: "", is_half_day: is_half_day})
        })
          .done(function( msg ) {
            console.log('workday was saved');
          });
});
