import requests, os

telegram_token = os.getenv('TELEGRAM_TOKEN')

def send(chat_id, ctx):
    msg = ""
    
    if(ctx["check"].status == "up"):
        msg = "Your check %s (%s) is up and has been pinged." % (ctx["check"].name, ctx["check"].code)

    if(ctx["check"].status == "down"):
        msg = "Your check %s (%s) is down" % (ctx["check"].name, ctx["check"].code)

    url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (telegram_token, chat_id, msg)
    return requests.get(url)

def get_user_id(data, username):
    for result in data['result']:
        if result['message']['from']['username'] == username:
            return result['message']['from']['id']
