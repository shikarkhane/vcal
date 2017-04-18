from app.mod_communicate.bl import Message

def unbooked_dates(event, context):
    '''If there are unbooked dates in next 30 days,
    after 2 days of term modification,
    send alert to admin'''

    Message("shikarkhane@gmail.com", "TERM_OPEN", ['vt2017']).send()
    print 'Event time was', event['time']
    print 'This log is', context.log_group_name, context.log_stream_name
    print 'Time left for execution:', context.get_remaining_time_in_millis()