import requests
import json

def test_scrape():
    url = "http://127.0.0.1:8000/api/v1/jobs/scrape"
    params = {
        "region": "San Francisco",
        "role": "Software Engineer"
    }
    
    try:
        print(f"Triggering scrape at {url}...")
        response = requests.post(url, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_scrape()
