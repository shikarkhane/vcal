function goto_invite(){
    $.cookie("show_work_step", 1, { path: '/' });
    window.location.replace("/sv/template/invite/");
}
$(".act-save-group").click(function(){
    name = $("#txt-create-group-name").val()
    type = $("#select-group-type").val()

    $.ajax({
          method: "POST",
          url: "/group/",
          data: { name: "John", location: "Boston" }
        })
          .done(function( msg ) {
            alert( "Data Saved: " + msg );
          });
});