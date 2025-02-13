import json, os
from flask import Flask, request, jsonify, abort
from datetime import datetime, timedelta, timezone
from openai import OpenAI
import httpx
from collections import deque
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# TODO: place your OpenAI base URL and OpenAI API key
BASE_URL = "OPENAI_BASE_URL"
API_KEY = "YOUR_API_KEY"

client = OpenAI(  
    base_url=BASE_URL, 
    api_key=API_KEY,
    http_client=httpx.Client(
        base_url=BASE_URL,
        follow_redirects=True,
    ),
)

timestamps = deque()

lock = threading.Lock()
def update_speed():
    now = datetime.now()
    with lock:
        timestamps.append(now)
        while timestamps and now - timestamps[0] > timedelta(seconds=10):  # Remove timestamps older than 10 seconds
            timestamps.popleft()
        rate = len(timestamps) / 10
        print("Current request rate:", rate, "req/s")


@app.route('/api/openai/chat_completion', methods = ["POST"])
def openai_completion():
    try:
        input_json = request.get_json()  # Extract input JSON from POST request
        print(input_json)  
        resp = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_json.get('prompt')}
            ],
            temperature=input_json.get('temperature'),
            max_tokens=input_json.get('max_tokens'),
            n=input_json.get('n')
        )
        # Convert response to a dictionary if it's not already
        if hasattr(resp, 'to_dict'):
            response_dict = resp.to_dict()
        else:
            response_dict = resp  # Assuming it's already a dict if not having to_dict method
        print(response_dict) 

    except Exception as e:
        print("[Error]:", str(e))
        return abort(500, str(e))
    
    update_speed()    
    return jsonify(response_dict) 

if __name__ == '__main__':
    app.run("0.0.0.0", port=9998)
