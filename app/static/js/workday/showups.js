
$("#confirm-showups").click(function(){
    work_date = $("#showup-chosen-date").val();
    workday_user_ids = [];
    standin_user_ids= [];
    $( ".cls-workday-date" ).each(function( index ) {
      workday_user_ids.push($( this ).attr("data-user-id"));
    });
    $( ".cls-standin-date" ).each(function( index ) {
      standin_user_ids.push($( this ).attr("data-user-id"));
    });

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/show-ups/",
          data: JSON.stringify({ group_id: 1, chosen_date: work_date,
          workday_user_ids: workday_user_ids, standin_user_ids: standin_user_ids})
        })
          .done(function( msg ) {
            console.log('showup was saved');
          });
});