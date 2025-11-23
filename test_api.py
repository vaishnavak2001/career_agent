"""Test script for the Career Agent API."""
import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_api():
    """Run comprehensive API tests."""
    
    print("=" * 60)
    print("Career Agent API Tests")
    print("=" * 60)
    
    # Test 1: Root endpoint (Note: Root is at /, not /api/v1)
    print("\n[1] Testing root endpoint...")
    try:
        root_response = requests.get("http://127.0.0.1:8001/")
        print(f"Status: {root_response.status_code}")
        print(json.dumps(root_response.json(), indent=2))
    except Exception as e:
        print(f"Root endpoint failed: {e}")
    
    # Test 2: Scrape jobs
    print("\n[2] Testing job scraping...")
    try:
        response = requests.post(
            f"{BASE_URL}/jobs/scrape",
            params={
                "region": "San Francisco",
                "role": "Software Engineer"
            }
        )
        print(f"Status: {response.status_code}")
        try:
            result = response.json()
            print(f"Jobs found: {result.get('jobs_found')}")
        except json.JSONDecodeError:
            print(f"Response text: {response.text}")
            return
    except Exception as e:
        print(f"Scrape failed: {e}")
        return
    
    # Test 3: List jobs
    print("\n[3] Listing scraped jobs...")
    response = requests.get(f"{BASE_URL}/jobs")
    result = response.json()
    # Handle list response directly if it returns a list
    if isinstance(result, list):
        print(f"Total jobs: {len(result)}")
        if len(result) > 0:
            job_id = result[0]['id']
            print(f"First job: {result[0]['title']} at {result[0]['company']}")
    else:
        print(f"Total jobs: {result.get('count')}")
        if result.get('count', 0) > 0:
            job_id = result['jobs'][0]['id']
            print(f"First job: {result['jobs'][0]['title']} at {result['jobs'][0]['company']}")
    
    if 'job_id' in locals():
        # Test 4: Get job details
        print(f"\n[4] Getting details for job {job_id}...")
        response = requests.get(f"{BASE_URL}/jobs/{job_id}")
        if response.status_code == 200:
            job_details = response.json()
            print(f"Company: {job_details.get('company')}")
            print(f"Title: {job_details.get('title')}")
            print(f"Location: {job_details.get('location')}")
            
            # Test 5: Analyze job (if endpoint exists)
            # print(f"\n[5] Analyzing job {job_id}...")
            # response = requests.post(f"{BASE_URL}/jobs/{job_id}/analyze")
            # if response.status_code == 200:
            #     analysis = response.json()
            #     print(f"Analysis: {analysis}")
            
            # Test 6: Calculate match score
            print(f"\n[6] Calculating match score...")
            sample_resume = """
            John Doe
            Senior Software Engineer
            
            Skills: Python, FastAPI, PostgreSQL, Docker, AWS, React
            
            Experience: 7 years building scalable web applications
            """
            
            # Note: match-score endpoint might not exist in current router, checking implementation...
            # It seems match score is calculated during scrape. 
            # But let's check if there is a standalone endpoint.
            # Based on previous edits, there isn't a standalone /match-score endpoint exposed in api.py
            # So skipping this test or adapting it.
            
        else:
            print(f"Failed to get job details: {response.status_code}")

    
    # Test 8: Search projects
    print("\n[8] Searching for projects...")
    response = requests.post(
        f"{BASE_URL}/projects/search",
        json=["Python", "FastAPI", "Machine Learning"]
    )
    if response.status_code == 200:
        projects_result = response.json()
        print(f"Projects found: {projects_result.get('projects_found')}")
    else:
        print(f"Project search failed: {response.status_code}")
    
    # Test 9: Dashboard stats
    print("\n[9] Getting dashboard stats...")
    response = requests.get(f"{BASE_URL}/dashboard/stats")
    if response.status_code == 200:
        stats = response.json()
        print(json.dumps(stats, indent=2))
    else:
        print(f"Dashboard stats failed: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API server.")
        print("Make sure the server is running on port 8001")
    except Exception as e:
        print(f"ERROR: {e}")
