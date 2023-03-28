from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import requests
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

class WhatsApp(BaseModel):
    template_name : str

# Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
# when starting the server
port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

# Open a ngrok tunnel to the dev server
public_url = ngrok.connect(port).public_url

'''
@function workingStatus
@description Check whether fastapi or ngrok working or not
'''
@app.get('/')
def workingStatus():
    return {'status' : "FastApi Connected to ngrok succesfully."}

# recipient : str, template_name : str
@app.post('/sendmessage')
async def message_to_user(template : WhatsApp):
    print("template : ", template)
    url = f"https://graph.facebook.com/{os.environ.get('VERSION')}/{os.environ.get('PHONE_NUMBER_ID')}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": os.environ.get('RECIPIENT_WA_ID'), 
        "type": "template", 
        "template": { 
            "name" : template.template_name,
            "language": { "code": "en_US" } 
            } 
    }
    print("url :",url)
    print("payload : ", payload)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('USER_ACCESS_TOKEN')}"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return {"message": "WhatsApp template message sent successfully!"}
    else:
        return {"message": f"Error sending WhatsApp template message: {response.text}"}


@app.post('/sendMedia')
async def send_media():
    pass

@app.post('/webhook')
async def whats_app_webhook():
    return {'Message' : "You reached to webhook succesfully..."}
