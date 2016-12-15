
$("#confirm-showups").click(function(){
    work_date = $("#showup-chosen-date").val();
    group_id = 1;
    workday_user_ids = [];
    standin_user_ids= [];
    $( ".cls-workday-date" ).each(function( index ) {
        if( this.checked ){
            workday_user_ids.push($( this ).attr("data-user-id"));
        }
    });
    $( ".cls-standin-date" ).each(function( index ) {
        if( this.checked ){
            standin_user_ids.push($( this ).attr("data-user-id"));
        }
    });

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/show-ups/" + group_id + "/date/" + work_date + "/",
          data: JSON.stringify({ workday_user_ids: workday_user_ids,
          standin_user_ids: standin_user_ids})
        })
          .done(function( msg ) {
            console.log('showup was saved');
          });
});