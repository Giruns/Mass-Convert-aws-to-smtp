import hmac
import hashlib
import base64
import os
import boto3



from sys import argv

from pyfiglet import Figlet


custom_fig = Figlet(font='graffiti')

print(custom_fig.renderText('CONVERT'))
print('\t Mass Convert aws to smtp | Get Limit Quota & Mail From')
print('\t By: Giruns\n')

# Values that are required to calculate the signature. These values should
# never change.
DATE = "11111111"
SERVICE = "ses"
MESSAGE = "SendRawEmail"
TERMINAL = "aws4_request"
VERSION = 0x04

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()



def calculateKey(pek):
   
    try:
        smtp = pek.split("|")
        idAccessKey = smtp[0] 
        secretAccessKey = smtp[1]
        region = smtp[2]
        choices=[
                'us-east-1',
                'us-east-2',
                'us-west-1',
                'us-west-2',
                'ap-south-1',
                'ap-northeast-3',
                'ap-northeast-2',
                'ap-southeast-1',
                'ap-southeast-2',
                'ap-northeast-1',
                'ca-central-1',
                'eu-central-1',
                'eu-west-1',
                'eu-west-2',
                'eu-west-3',
                'eu-north-1',
                'sa-east-1',
                'ca-central-2'
            ]
        if region not in choices:
            print(idAccessKey+ ' Error InvalidClientTokenId!')

        else:
            client = boto3.client(
                'ses',
                aws_access_key_id=idAccessKey,
                aws_secret_access_key=secretAccessKey,
                region_name=region)
            response = client.get_send_quota()
            mail = client.list_identities(
                IdentityType='EmailAddress',
                MaxItems=123,
                NextToken='',
                )

            if 'Max24HourSend' in response:

                signature = sign(("AWS4" + secretAccessKey).encode('utf-8'), DATE)
                signature = sign(signature, region)
                signature = sign(signature, SERVICE)
                signature = sign(signature, TERMINAL)
                signature = sign(signature, MESSAGE)
                signatureAndVersion = bytes([VERSION]) + signature
                smtpPassword = base64.b64encode(signatureAndVersion)
                print('Converted! Saved! | '+smtpPassword.decode('utf-8')+' | Max24HourSend:'+str(response['Max24HourSend'])+ '| SentLast24Hours:'+str(response['SentLast24Hours']))
                
                tot = len(mail['Identities'])
                if tot >= 1:
                    # for x in range(tot):
                    
                    print(' Mail from:'+mail['Identities'][1])
                    print('____________________________')
                    xx = str('email-smtp.'+region+'.amazonaws.com|587|'+idAccessKey+'|'+smtpPassword.decode('utf-8')+'|'+mail['Identities'][1]+'|'+str(response['Max24HourSend'])+'|'+str(response['SentLast24Hours'])).replace('\r', '')
                    save = open('smtpaws.txt', 'a')
                    save.write(xx+'\n')
                    save.close()    

                else:
                    
                    print(' Mail from: [null] Check manual')
                    print('____________________________')
                    xx = str('email-smtp.'+region+'.amazonaws.com|587|'+idAccessKey+'|'+smtpPassword.decode('utf-8')+'|mailform@cek.manual|'+str(response['Max24HourSend'])+'|'+str(response['SentLast24Hours'])).replace('\r', '')
                    save = open('smtpaws.txt', 'a')
                    save.write(xx+'\n')
                    save.close()
            

            else:
                print(idAccessKey+' Error InvalidClientTokenId!')

        
        

    except Exception as e:
        print('')
        print(str(e))
        print('____________________________') 
    

aws = open(argv[1], 'r').read().split('\n')

for wsa in aws:
    if '|' not in wsa:
        print('')
        print(' Error. Line no value !')
        print('____________________________') 
    

    else:
        calculateKey(wsa)


# { SECMTP - SECRET TO SMTP }

# command ?

# python mws.py list.txt
# test by python 3.8 | wndows 10 server 2012 
# __________
# Format list :

# AKIAXZG6PFKAACQXCQWU|QF9cuUlmNuiDmH3MlHXNKgOy2qXOgr1gyMKz4LwL|us-east-1
# AKIAJXX4J3PRZFALLO2A|uz4z9VWpbOxp5yHgFsWbwezCJkEEzgz36laH3uT6|ap-southeast-1
# AKIAS7R5HVQO3OVKMDWR|/cINXvn24iVFd32eORL0v5whqSYWOViMQ4cO3+EZ|aws_unknown_regio
# __________


# Result smtp:

# email-smtp.us-east-1.amazonaws.com|587|AKIAXZG6PFKAACQXCQWU|BAQbfnjhyet4Kz3h9RWKl0w+09Sd3QfsSJGR+bb2r4ma|kajiyama@oblik.co.jp|50000.0|0.0
