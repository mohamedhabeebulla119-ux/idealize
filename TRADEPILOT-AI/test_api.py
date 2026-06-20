import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:8000/api"

# Wait a moment for the server to start if run sequentially
time.sleep(2)

def test_endpoint(endpoint: str, payload: dict):
    # Sleep to avoid hitting Gemini Free Tier rate limits (15 RPM)
    print("Waiting 5 seconds to avoid API rate limits...")
    time.sleep(5)
    
    url = f"{API_BASE_URL}/{endpoint}"
    print(f"\n--- Testing POST {url} ---")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Success! Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Failed! Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Details: {e.response.text}")

if __name__ == "__main__":
    scenario_payload = {
        "trade_type": "import",
        "product": "Medical Devices",
        "country": "Germany"
    }

    # 1. Test Compliance Endpoint
    test_endpoint("compliance", scenario_payload)

    # 2. Test Workflow Endpoint
    test_endpoint("workflow", scenario_payload)

    # 3. Test Checklist Endpoint (Adding doc fields)
    checklist_payload = {**scenario_payload, "documents": ["Invoice"], "approvals": []}
    test_endpoint("checklist", checklist_payload)

    # 4. Test Documents Endpoint
    test_endpoint("documents", scenario_payload)

    # 5. Test Cost Estimation Endpoint
    cost_payload = {
        "product": "Medical Devices",
        "country": "Germany",
        "product_value": 50000.0
    }
    test_endpoint("cost-estimation", cost_payload)

    # 6. Test Tariff Search Endpoint
    tariff_payload = {
        "product": "Medical Devices",
        "hs_code": "9018"
    }
    test_endpoint("tariff-search", tariff_payload)

    # 7. Test Advanced RAG: Casual Greeting
    greeting_payload = {
        "query": "Hi there! How are you doing today?"
    }
    test_endpoint("intent", greeting_payload)

    # 8. Test Advanced RAG: Complex Decomposition
    complex_payload = {
        "query": "What are the customs duties for Cinnamon and how do I get an export license?"
    }
    test_endpoint("intent", complex_payload)

