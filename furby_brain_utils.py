import requests
import json
import unicodedata

def ollama_chat(prompt, model="deepseek-r1:1.5b"):
    url = "http://localhost:11434/api/generate"
    headers = {"content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Set to True for streaming responses
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=90)
        response.raise_for_status()
        return response.json().get("response", "[No response]")
    except requests.exceptions.RequestException as e:
        return f"[Error connecting to Ollama: {e}]"    

def clean_response(text):
    return text.rsplit("</think>", 1)[-1].strip()  # Removes the thinking portion of the response from Deep Seek

def sanitize(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
