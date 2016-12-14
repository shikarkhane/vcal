
$("#confirm-showups").click(function(){
    work_date = $("#showup-chosen-date").val();

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/show-ups/",
          data: JSON.stringify({ group_id: 1, work_date: work_date,
          workday_user_ids: [1,2,3], standin_user_ids: [23]})
        })
          .done(function( msg ) {
            console.log('showup was saved');
          });
});