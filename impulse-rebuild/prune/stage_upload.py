#!/usr/bin/env python3
"""POST a file to a Shopify staged-upload target using the returned parameters."""
import json, sys, urllib.request, mimetypes, uuid, os

cfg = json.load(open(sys.argv[1]))
body = []
boundary = uuid.uuid4().hex
def part(name, value):
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())

for name, value in cfg['params']:
    part(name, value)

data = open(cfg['file'], 'rb').read()
fname = os.path.basename(cfg['file'])
body.append(
    f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\n'
    f'Content-Type: text/csv\r\n\r\n'.encode() + data + b'\r\n')
body.append(f'--{boundary}--\r\n'.encode())
payload = b''.join(body)

req = urllib.request.Request(cfg['url'], data=payload, method='POST')
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        print("HTTP", r.status)
        print(r.read().decode()[:600])
except urllib.error.HTTPError as e:
    print("HTTPError", e.code)
    print(e.read().decode()[:800])
except Exception as e:
    print("ERR", type(e).__name__, e)
