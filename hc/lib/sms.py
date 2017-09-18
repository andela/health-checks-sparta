from twilio.rest import Client
from ..local_settings import TWILIO
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = TWILIO["account_sid"]
auth_token = TWILIO["auth_token"]

client = Client(account_sid, auth_token)

def send(to, ctx):
    msg = "" # compose message
    
    if(ctx["check"].status == "up"):
        msg = "Your check %s (%s) is up and has been pinged" % (ctx["check"].name, ctx["check"].code)

    if(ctx["check"].status == "down"):
        msg = "Your check %s (%s) is down" % (ctx["check"].name, ctx["check"].code)

    try:
        client.messages.create(
            body=msg,
            to=to,
            from_=TWILIO["from_"])
            
    except Exception as error:
        print(error)
