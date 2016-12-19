$( document ).ready(function() {
    group_id = 1;

    $.ajax({
          contentType : 'application/json',
          method: "GET",
          url: "/sv/work-sign-up/" + group_id + "/"
          // ,data: JSON.stringify({ workday_user_ids: workday_user_ids, standin_user_ids: standin_user_ids})
        })
          .done(function( msg ) {
            console.log('get work sign up');
          });

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

