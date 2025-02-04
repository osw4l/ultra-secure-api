import os
import httpx
import asyncio
import json


async def send_email(email: str, subject: str, content: str):
    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {os.environ.get('SENDGRID_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "personalizations": [{
            "to": [{"email": email}]
        }],
        "from": {"email": os.environ.get('SENDGRID_EMAIL_SENDER')},
        "subject": subject,
        "content": [{
            "type": "text/html",
            "value": content
        }]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print("Status Code:", response.status_code)
            print("Response Body:", response.text)
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
