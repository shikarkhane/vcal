
$(".act-send-invites").click(function(){
    emails = $("#textarea-invitees").val().split(',');
    group_id = 1;

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/invite/",
          data: JSON.stringify({ group_id: group_id, emails: emails })
        })
          .done(function( msg ) {
                console.log('invites sent');
          });

});


$(".act-invite-nextstep").click(function(){
    if ( $.cookie("show_work_step") == 1){
        window.location.replace("/sv/template/work-day/");
    }
});