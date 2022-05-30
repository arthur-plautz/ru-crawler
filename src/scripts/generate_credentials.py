from email.mime import base
import json
import base64

creds_file = open('credentials.json')
creds = json.load(creds_file)
users = str(creds.get('users')).encode('ascii')

print(base64.b64encode(users).decode('ascii'))