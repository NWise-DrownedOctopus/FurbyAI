import requests
import json

def ollama_chat(prompt, model="deepseek-r1:1.5b"):
    url = "http://localhost:11434/api/generate"
    headers = {"content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Set to True if you want streaming responses
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def clean_response(text):
    return text.rsplit("</think>", 1)[-1].strip()  # Get the last part after the last "</think>"
