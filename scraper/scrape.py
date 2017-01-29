import http.client
import getpass

def default_headers(client, cookies = None):
    client.putheader('Accept', 'text/html')
    client.putheader('Accept-Language', 'en-US')
    client.putheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    if cookies is not None:
        print ('; '.join(cookies))
        client.putheader('Cookie', '; '.join(cookies))

base_url = 'battleofthebits.org'
base_dir = '/arena/Entry/botb-scraper/'
base_login = '/barracks/Login/'
req_boundary = '----BotBScraperBoundary'

# Get session cookies which allows for downloading BotB content
print('Please sign into BotB')
botb_user = input(' email: ')
botb_pass = getpass.getpass(' password: ')

# Get PHP SessionID
client = http.client.HTTPConnection(base_url)
client.connect()
client.putrequest("GET", '/')
default_headers(client)
client.endheaders()
response = client.getresponse()
# Get cookie through black magic
php_session = [header[1] for header in response.getheaders() if header[0] == 'Set-Cookie'][0]
php_session = php_session[:php_session.index(";")-1]
client.close()

# Sign into BotB using the provided credidentials
client.putrequest("POST", base_login)
default_headers(client)
client.putheader('Content-Type', 'multipart/form-data; boundary=' + req_boundary)
client.putheader('Cookie', php_session)

# Build the request payload
payload = '--' + req_boundary + '\n'
payload += 'Content-Disposition: form-data; name="email"\n'
payload += '\n'
payload += botb_user + '\n'
payload += '--' + req_boundary + '\n'
payload += 'Content-Disposition: form-data; name="password"\n'
payload += '\n'
payload += botb_pass + '\n'
payload += '--' + req_boundary + '\n'
payload += 'Content-Disposition: form-data; name="submitok"\n'
payload += '\n'
payload += 'LOGIN\n'
payload += '--' + req_boundary
client.putheader('Content-Length', len(payload))
client.endheaders()
client.send(payload.encode())

response = client.getresponse()

# In addition to our php session, we now have 3 more cookies that are used...
# user_id, serial, and botbr_id. These 3 plus the session id allow for using
# BotB to it's fullest extent!
botb_cookies = []
botb_cookies.append(php_session)
for header in response.getheaders():
    if header[0] == 'Set-Cookie':
        botb_cookies.append(header[1][:header[1].index(';')])
client.close()

# Load up the BotB homepage, allowing us to get the user and their points etc
# Havin some fun here w/ the scraper.
client = http.client.HTTPConnection(base_url)
client.connect()
client.putrequest("GET", '/')
default_headers(client, botb_cookies)
client.endheaders()
response = client.getresponse()
print(str(response.read()))
client.close()
