
$(".act-workday-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/sv/rule/");
    }
});

$("#create-workday-save").click(function(){
    //w = Workday(d['created_by_id'], d['group_id'], d['work_date'], d['standin_count'], d['from_time'], d['to_time'])
    work_date = $("#create-workday-date").val();
    standin_count = $("#create-workday-standin-count").val();
    from_time = $("#create-workday-fromtime").val();
    to_time = $("#create-workday-totime").val();

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/workday/",
          data: JSON.stringify({ created_by_id: 1, group_id: 1, work_date: work_date, standin_count: standin_count,
          from_time: from_time, to_time: to_time})
        })
          .done(function( msg ) {
            console.log('workday was saved');
          });
});
