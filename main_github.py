from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv
load_dotenv()
import http
import hashlib
import hmac
import os
from pyngrok import ngrok
import sys
import json

app = FastAPI()

# Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
# when starting the server
port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

# Open a ngrok tunnel to the dev server
public_url = ngrok.connect(port).public_url
print(public_url)

'''
@function workingStatus
@description Check whether fastapi or ngrok working or not
'''
@app.get('/')
def workingStatus():
    return {'status' : "FastApi Connected to ngrok succesfully."}

'''
@function generate_hash_signature
@description generate the hash signature using secret key
'''
def generate_hash_signature(secret : bytes, payload : bytes, digest_method = hashlib.sha1):
    return hmac.new(secret, payload, digest_method).hexdigest()



'''
@function gitHubWebhook
@description get the event occured by the github
'''
@app.post('/gitwebhook', status_code=http.HTTPStatus.ACCEPTED)
async def gitHubWebhook(request : Request, x_hub_signature : str = Header(None)):
    try:
        payload = await request.body() # return a class of bytes
        json_body = json.loads(payload.decode("utf-8")) # 
        secret = os.environ.get('WEBHOOK_SECRET').encode('utf-8')
        signature = generate_hash_signature(secret, payload)
        print('Signature : ',signature)
        if x_hub_signature != f"sha1={signature}":
            raise HTTPException(status_code=401, detail='Authentication error.')
        with open('gitpushevent.json','w') as jfile:
            json.dump(json_body,jfile)
        return {'Status' : 'Get the event details and stored in file succesfully.'}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'{e}')
