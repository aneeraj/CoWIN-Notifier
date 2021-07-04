import requests
import json
import os

from twilio.rest import Client
from datetime import date, timedelta

def makecall():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                        twiml='<Response><Say>Vaccine is now available!</Say></Response>',
                        to='+91XXXXXX', # To Phone Number
                        from_='+XXXXXX' # From Phone Number
                    )

    print(call.sid)

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ['TELEGRAM_TOKEN'] #Enter Telegram Bot Token
    bot_chatID = os.environ['TELEGRAM_CHATID'] #Enter Telgram Chat ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    makecall()
    return response.json()

today = date.today()
d1 = today + timedelta(days=1)
d = d1.strftime("%d/%m/%Y")
print(d)
url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByCenter'

params = dict(
    center_id='579488',  #For Atreya= 579488
    date=d,
)

resp = requests.get(url=url, params=params)
data = resp.json()
#print (data['centers']['sessions'][0]['available_capacity_dose1'])

for key in data['centers']['sessions']:
    if key['min_age_limit'] == 18 and key['available_capacity_dose1'] > 0:
        my_message = "Vaccine available for: " + key['date'] + " at " + data['centers']['name']
        telegram_bot_sendtext(my_message)