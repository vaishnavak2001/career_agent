"""
API Service for Frontend Integration
"""
import requests
    from typing import Dict, List

BASE_URL = "http://127.0.0.1:8000/api/v1"

class APIService:
@staticmethod
    def get_jobs(skip: int = 0, limit: int = 100) -> List[Dict]:
"""Fetch jobs from API"""
try:
response = requests.get(f"{BASE_URL}/jobs/", params = { "skip": skip, "limit": limit })
return response.json() if response.status_code == 200 else[]
        except Exception as e:
print(f"Error fetching jobs: {e}")
return []

@staticmethod
    def trigger_scrape(region: str, role: str) -> Dict:
"""Trigger job scraping"""
try:
response = requests.post(f"{BASE_URL}/jobs/scrape", params = { "region": region, "role": role })
return response.json() if response.status_code == 200 else { "error": "Failed" }
        except Exception as e:
return { "error": str(e) }
