# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

def init_sms(phone_list, msg):
    """ Send text message to each phone number from the phone_list with msg as attachment """

    for phone in phone_list:
        message = client.messages \
                        .create(
                            # msg="Xin chào! Rất vui được gặp bạn",
                            body = msg,
                            media_url=['https://www.plannedparenthoodaction.org/uploads/filer_public_thumbnails/filer_public/59/eb/59eb4066-411b-479c-a705-903e08a41faf/mnsure_2019_oe_1200x628.png__800x600_q75_subsampling-2.jpg'],
                            from_='+15705255806',
                            to=phone
                        )
    return message.sid
def mock_init_sms(phone_list, msg):
    """ Send text message to each phone number from the phone_list with msg as attachment """
    print(f'sms.py {msg}')
    print(f'length of phone_list {len(phone_list)}')
    for phone in phone_list:
        print(f'Mock text to {phone}')
    message = client.messages \
                    .create(
                        # body="From Kim Nghiem: Xin chào! Rất vui được gặp bạn",
                        body = msg,
                        #media_url=['https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg'],
                        #media_url=['http://www.rareseeds.com/assets/1/14/DimThumbnail/Jubilee-Watermelon-web.jpg'],
                        media_url=['https://www.plannedparenthoodaction.org/uploads/filer_public_thumbnails/filer_public/59/eb/59eb4066-411b-479c-a705-903e08a41faf/mnsure_2019_oe_1200x628.png__800x600_q75_subsampling-2.jpg'],

                        from_='+15705255806',
                        to='+16129780575'                       )
        
    return message.sid