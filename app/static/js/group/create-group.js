
$(".act-save-group").click(function(){
    name = $("#txt-create-group-name").val()
    type_id = $("#select-group-type").val()

    $.cookie("show_work_step", 1, { path: '/' });

    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/group/",
          data: JSON.stringify({ name: name, type_id: type_id })
        })
          .done(function( msg ) {
            // alert( "Data Saved: " + msg );
            if ( $.cookie("show_work_step") == 1){
                window.location.replace("/sv/invite/");
            }
          });

});