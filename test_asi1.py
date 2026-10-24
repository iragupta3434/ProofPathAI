
import os
import requests
from getpass import getpass

api_key = getpass("Paste your ASI:One API key: ")

url = "https://api.asi1.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "asi1",
    "messages": [
        {
            "role": "user",
            "content": "Hello! Reply briefly and confirm you are working."
        }
    ]
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()
    result = response.json()

    print("\nASI:One response:")
    print(result["choices"][0]["message"]["content"])

except requests.exceptions.HTTPError:
    print("API error:", response.status_code)
    print(response.text)

except requests.exceptions.RequestException as error:
    print("Connection error:", error)
