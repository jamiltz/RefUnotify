from twilio.rest import TwilioRestClient
import urllib
import cgi
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

#User Details
userTel = "447887495965"
fromTel = "+442033223829"
messageBody = "We are Ready to Rock"

account= os.environ['ACCOUNT']
token = os.environ['TOKEN']
client = TwilioRestClient(account, token)

#using TwilioRestClient
#message = client.sms.messages.create(to=userTel, from_="+"+fromTel,
#                                     body=messageBody)

# Message is sent using RU api
def sendMessage(tel, msg):
  #Using RS  provided SMS code
  encodedMsg = urllib.quote(msg)

  urllib.urlopen('http://sms.api.refunite.org/?password=179d50c6eb31188925926a5d1872e8117dc58572&number='+tel+'&message='+encodedMsg)
  print 'Message sent to user as tel:' + tel + ' and encodedMsg:' + encodedMsg

def TwilioCall(tel, msg):
  call = client.calls.create(to=tel, 
                           from_=fromTel, 
                           url="http://www.necto.me/notify.xml")
  #print call.sid
#print "Message Sent"	#debug
# The web server.
class MyHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path == '/notify':
      form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
        environ={'REQUEST_METHOD':'POST'})
      number = form['number'].value
      body = form['body'].value
      print 'Got Number:', number	#debug
      print 'Got Message Body: ', body	#debug
      TwilioCall(number, body)
      sendMessage(number, body)
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      return
    #Response Sent from Twilio API's
    elif self.path == '/twiresponse':
      form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
      environ={'REQUEST_METHOD':'POST'})
      data = form['data'].value
      body = form['body'].value
      print 'TGot data:', data	#debug
      #print 'TGot Message Body: ', body	#debug
      #sendMessage(number, body)
      return
    return self.do_GET()

# Server Message local post server
server = HTTPServer(('', 8080), MyHandler).serve_forever()
