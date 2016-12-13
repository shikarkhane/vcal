
$("#create-summon-save").click(function(){
    work_date = $("#create-summon-date").val();
    from_time = $("#create-summon-fromtime").val();
    to_time = $("#create-summon-totime").val();

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/summon/",
          data: JSON.stringify({ created_by_id: 1, group_id: 1, work_date: work_date,
          from_time: from_time, to_time: to_time})
        })
          .done(function( msg ) {
            console.log('summon was saved');
          });
});
