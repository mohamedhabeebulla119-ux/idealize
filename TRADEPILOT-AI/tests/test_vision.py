import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def test_vision():
    endpoint = f"{API_BASE_URL}/document-verification/"
    
    # Create a dummy invoice in memory
    dummy_invoice_text = """
    COMMERCIAL INVOICE
    ------------------
    Invoice Number: INV-2023-991
    Date: 2023-10-15
    Exporter: Germany Medical Corp
    Importer: Sri Lanka Health Ministry
    
    Item: 50x MRI Machines
    Total Value: $50,000 USD
    
    Signature: [Unsigned]
    """
    
    # We will upload it as a text file for testing, Gemini supports text/plain
    files = {
        "file": ("invoice.txt", dummy_invoice_text, "text/plain")
    }
    
    data = {
        "document_type": "Commercial Invoice",
        "expected_standards": "Must contain Invoice Number, Date, Total Value, and a valid Signature."
    }
    
    print(f"--- Testing POST {endpoint} ---")
    try:
        response = requests.post(endpoint, files=files, data=data)
        if response.status_code == 200:
            print("Success! Response:")
            import json
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed. Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vision()
