$( document ).ready(function() {
    /*
    get pending day count
    $.ajax({
          contentType : 'application/json',
          method: "GET",
          url: "/sv/show-ups/" + group_id + "/date/" + work_date + "/",
          data: JSON.stringify({ workday_user_ids: workday_user_ids,
          standin_user_ids: standin_user_ids})
        })
          .done(function( msg ) {
            console.log('showup was saved');
          });
          */
});


$(".cls-worksignup-term").change(function(){
    term_id = $( this ).attr("data-term-id");
    //show pending days for the term selected
});


$(".cls-worksignup-standin").change(function(){
    chosen_date = $( this ).attr("data-date");
    //show pending days for the term selected
});


$(".cls-worksignup-workday").change(function(){
    chosen_date = $( this ).attr("data-date");
    //show pending days for the term selected
});


$(".cls-worksignup-more-standin").click(function(){
    last_date = $( this ).attr("data-last-date");
    //show pending days for the term selected
});

$(".cls-worksignup-more-workday").click(function(){
    last_date = $( this ).attr("data-last-date");
    //show pending days for the term selected
});

