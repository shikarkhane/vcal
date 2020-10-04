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
    $.ajax({
          contentType : 'application/json',
          method: "GET",
          url: "/sv/term_details/" + group_id + "/"
        })
          .done(function( msg ) {
            console.log(msg);
          });

});


$(".cls-worksignup-term").change(function(){
    term_id = $( this ).attr("data-term-id");
    console.log('last date'+ last_date);
});


$(".cls-worksignup-standin").change(function(){
    chosen_date = $( this ).attr("data-date");
    user_id = 23;
    is_workday = false;
    is_taken = false;
    if( this.checked ){
            is_taken = true;
        }

     $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/work-sign-up/" + group_id + "/",
          data: JSON.stringify({ chosen_date: chosen_date, user_id: user_id,
          is_workday: is_workday, is_taken: is_taken})
        })
          .done(function( msg ) {
            console.log('work sign up - stand in saved');
          });
});


$(".cls-worksignup-workday").change(function(){
    chosen_date = $( this ).attr("data-date");
    user_id = 23;
    is_workday = true;
    is_taken = false;
        if( this.checked ){
                is_taken = true;
            }

     $.ajax({
          contentType : 'application/json',
          method: "POST",
          url: "/sv/work-sign-up/" + group_id + "/",
          data: JSON.stringify({ chosen_date: chosen_date, user_id: user_id,
          is_workday: is_workday, is_taken: is_taken})
        })
          .done(function( msg ) {
            console.log('work sign up - workday saved');
          });
});


$(".cls-worksignup-more-standin").click(function(){
    last_date = $( this ).attr("data-last-date");
    console.log('last date'+ last_date);
});

$(".cls-worksignup-more-workday").click(function(){
    last_date = $( this ).attr("data-last-date");
    console.log('last date'+ last_date);
});

