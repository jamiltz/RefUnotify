from twilio.rest import TwilioRestClient

#User Details
userTel = "+447887495965"
fromTel = "+442033223829"
messageBody = "We are Ready to Rock"

account= os.environ['ACCOUNT']
token = os.environ['TOKEN']
client = TwilioRestClient(account, token)

#using TwilioRestClient
message = client.sms.messages.create(to=userTel, from_=fromTel,
                                     body=messageBody)

print "Message Sent"	#debug
