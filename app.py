from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

app = FastAPI()

# Load your service account credentials
SERVICE_ACCOUNT_FILE = 'safezone-973d7-firebase-adminsdk-3661h-6aaf47e0ba.json'
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

@app.get("/send-notification/")
async def send_notification(token: str, message: str):
    # Create a credentials object from the service account file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Refresh the credentials to get the access token
    credentials.refresh(Request())
    access_token = credentials.token

    # Prepare the FCM message
    fcm_url = "https://fcm.googleapis.com/v1/projects/speakout-34985/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": "Safe Zone Notification",
                "body": message
            }
        }
    }

    # Send the FCM message
    response = requests.post(fcm_url, headers=headers, json=payload)

    return JSONResponse(status_code=response.status_code, content=response.json())
