import os
from twilio.rest import Client

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_ = os.getenv('TWILIO_FROM_')

#client = Client(account_sid, auth_token)

def send(to, ctx):
    msg = ""
    
    if(ctx["check"].status == "up"):
        msg = "Your check %s (%s) is up and has been pinged" % (ctx["check"].name, ctx["check"].code)

    if(ctx["check"].status == "down"):
        msg = "Your check %s (%s) is down" % (ctx["check"].name, ctx["check"].code)

    try:
        client.messages.create(
            body=msg,
            to=to,
            from_=from_)
            
    except Exception as error:
        print(error)
