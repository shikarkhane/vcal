$(".children-radio").click(function(){
    term_id = $(this).closest(".term-children").attr("data-term-id");
    child_count = $(this).attr('data-child-count');
    $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/children/",
          data: JSON.stringify({ term_id: term_id, child_count: child_count})
        })
          .done(function( msg ) {
            console.log('term child count saved');
          });

});
