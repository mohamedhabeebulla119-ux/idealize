import requests

BASE_URL = "http://localhost:8000"  # default port for uvicorn, let's see if we can find the port in config or logs

# Let's try calling health check on 8000 and 49690 (which is the browser dev server port or maybe backend port)
for port in [8000, 49690]:
    try:
        r = requests.get(f"http://localhost:{port}/health")
        if r.status_code == 200:
            print(f"Server is running on port {port}!")
            BASE_URL = f"http://localhost:{port}"
            break
    except Exception:
        pass

print(f"Using BASE_URL: {BASE_URL}")

# Test Chat
chat_payload = {
    "message": "Hi, what is TradePilot AI?",
    "history": []
}

try:
    response = requests.post(f"{BASE_URL}/api/chat/chat", json=chat_payload)
    print("Chat Response Status:", response.status_code)
    print("Chat Response Content:", response.json())
except Exception as e:
    print("Failed to chat:", e)
