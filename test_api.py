"""Test script for the Career Agent API."""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_api():
    """Run comprehensive API tests."""
    
    print("=" * 60)
    print("Career Agent API Tests")
    print("=" * 60)
    
    # Test 1: Root endpoint (Note: Root is at /, not /api/v1)
    print("\n[1] Testing root endpoint...")
    root_response = requests.get("http://127.0.0.1:8000/")
    print(f"Status: {root_response.status_code}")
    print(json.dumps(root_response.json(), indent=2))
    
    # Test 2: Scrape jobs
    print("\n[2] Testing job scraping...")
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
    
    # Test 3: List jobs
    print("\n[3] Listing scraped jobs...")
    response = requests.get(f"{BASE_URL}/jobs")
    result = response.json()
    print(f"Total jobs: {result.get('count')}")
    if result['count'] > 0:
        job_id = result['jobs'][0]['id']
        print(f"First job: {result['jobs'][0]['title']} at {result['jobs'][0]['company']}")
    
        # Test 4: Get job details
        print(f"\n[4] Getting details for job {job_id}...")
        response = requests.get(f"{BASE_URL}/jobs/{job_id}")
        job_details = response.json()
        print(f"Company: {job_details['company']}")
        print(f"Title: {job_details['title']}")
        print(f"Location: {job_details['location']}")
        
        # Test 5: Analyze job
        print(f"\n[5] Analyzing job {job_id}...")
        response = requests.post(f"{BASE_URL}/jobs/{job_id}/analyze")
        analysis = response.json()
        print(f"Skills found: {analysis['parsed_data']['skills']}")
        print(f"Seniority: {analysis['parsed_data']['seniority']}")
        print(f"Is scam: {analysis['scam_detection']['is_scam']}")
        
        # Test 6: Calculate match score
        print(f"\n[6] Calculating match score...")
        sample_resume = """
        John Doe
        Senior Software Engineer
        
        Skills: Python, FastAPI, PostgreSQL, Docker, AWS, React
        
        Experience: 7 years building scalable web applications
        """
        
        response = requests.post(
            f"{BASE_URL}/match-score",
            json={
                "resume_text": sample_resume,
                "job_id": job_id
            }
        )
        match_result = response.json()
        print(f"Match Score: {match_result['match_score']}/100")
        
        # Test 7: Generate cover letter
        print(f"\n[7] Generating cover letter...")
        response = requests.post(
            f"{BASE_URL}/cover-letter/generate",
            json={
                "job_id": job_id,
                "resume_text": sample_resume,
                "personality": "professional"
            }
        )
        cover_letter_result = response.json()
        print(f"Personality: {cover_letter_result['personality']}")
        print(f"Cover Letter Preview:\n{cover_letter_result['cover_letter'][:200]}...")
    
    # Test 8: Search projects
    print("\n[8] Searching for projects...")
    response = requests.post(
        f"{BASE_URL}/projects/search",
        json=["Python", "FastAPI", "Machine Learning"]
    )
    projects_result = response.json()
    print(f"Projects found: {projects_result['projects_found']}")
    
    # Test 9: Dashboard stats
    print("\n[9] Getting dashboard stats...")
    response = requests.get(f"{BASE_URL}/dashboard/stats")
    stats = response.json()
    print(json.dumps(stats, indent=2))
    
    # Test 10: Match distribution
    print("\n[10] Getting match score distribution...")
    response = requests.get(f"{BASE_URL}/analytics/match-distribution")
    distribution = response.json()
    print(json.dumps(distribution, indent=2))
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API server.")
        print("Make sure the server is running with: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"ERROR: {e}")
