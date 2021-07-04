import requests
import json
import os

from twilio.rest import Client
from datetime import date, timedelta
flag = 0
my_message =''
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
#   makecall() //Uncomment to enable call notifications
    return response.json()

today = date.today()
d1 = today + timedelta(days=1)
d = d1.strftime("%d/%m/%Y")
print(d)
url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict'

params = dict(
    district_id='303',  #For Thrissur = 303
    date=d,
)

resp = requests.get(url=url, params=params)
data = resp.json()

for key in data['sessions']:
    if key['min_age_limit'] == 18 and key['available_capacity_dose1'] > 0:
        my_message += str(key['available_capacity_dose1']) + " " + key['vaccine'] + " vaccine available for: " + key['date'] + " at " + key['name'] + " Fee-Type:" + key['fee_type'] + "\n"
        flag = 1
if flag == 1:        
    telegram_bot_sendtext(my_message)