import requests
from ..local_settings import TELEGRAM

def send(chat_id, ctx):
    msg = "" # compose message
    
    if(ctx["check"].status == "up"):
        msg = "Your check %s (%s) is up and has been pinged." % (ctx["check"].name, ctx["check"].code)

    if(ctx["check"].status == "down"):
        msg = "Your check %s (%s) is down" % (ctx["check"].name, ctx["check"].code)

    url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (TELEGRAM['token'], chat_id, msg)
    return requests.get(url)

def get_user_id(data, username):
    for result in data['result']:
        if result['message']['from']['username'] == username:
            return result['message']['from']['id']
