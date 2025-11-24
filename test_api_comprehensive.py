"""Comprehensive API endpoint testing for Phase 2."""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8888"
API_URL = f"{BASE_URL}/api/v1"

def print_test_header(title: str):
    """Print formatted test section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_endpoint(method: str, endpoint: str, data: Dict[Any, Any] = None, files: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Test an API endpoint and return results."""
    url = f"{API_URL}{endpoint}"
    print(f"\n[TEST] {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print(f"[ERROR] Unsupported method: {method}")
            return {"error": "Unsupported method"}
        
        print(f"[RESPONSE] Status: {response.status_code}")
        
        try:
            result = response.json()
            print(f"[DATA] {json.dumps(result, indent=2)[:500]}...")  # First 500 chars
            return {"status": response.status_code, "data": result}
        except:
            print(f"[DATA] {response.text[:200]}")
            return {"status": response.status_code, "text": response.text}
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection failed - Is the server running?")
        return {"error": "Connection failed"}
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": str(e)}

def run_all_tests():
    """Run all API endpoint tests."""
    
    print("\n" + "="*60)
    print("  CAREER AGENT - COMPREHENSIVE API TEST SUITE")
    print("  Phase 2: Application Logic Testing")
    print("="*60)
    
    results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # Test 1: Root Endpoint
    print_test_header("1. ROOT & HEALTH ENDPOINTS")
    r1 = test_endpoint("GET", "/../../")  # Root endpoint
    if r1.get("status") == 200:
        results["passed"] += 1
    else:
        results["failed"] += 1
        results["errors"].append("Root endpoint failed")
    
    r2 = test_endpoint("GET", "/../../health")
    if r2.get("status") == 200:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 2: Jobs Endpoints
    print_test_header("2. JOBS ENDPOINTS")
    
    # Get all jobs
    jobs_result = test_endpoint("GET", "/jobs/")
    if jobs_result.get("status") == 200:
        results["passed"] += 1
        jobs = jobs_result.get("data", [])
        print(f"[INFO] Found {len(jobs)} jobs in database")
        
        # Test job scraping (if Adzuna API is configured)
        print("\n[TEST] Testing job scraping...")
        scrape_result = test_endpoint("POST", "/jobs/scrape?region=Remote&role=Software%20Engineer")
        if scrape_result.get("status") in [200, 422]:  # 422 if no API key
            results["passed"] += 1
        else:
            results["failed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: Dashboard Endpoints
    print_test_header("3. DASHBOARD ENDPOINTS")
    
    stats_result = test_endpoint("GET", "/dashboard/stats")
    if stats_result.get("status") == 200:
        results["passed"] += 1
        stats = stats_result.get("data", {})
        print(f"[INFO] Dashboard stats:")
        print(f"  Jobs scraped: {stats.get('jobs_scraped', 0)}")
        print(f"  Applications: {stats.get('applications_sent', 0)}")
        print(f"  Scams blocked: {stats.get('scams_blocked', 0)}")
    else:
        results["failed"] += 1
    
    dist_result = test_endpoint("GET", "/dashboard/match-distribution")
    if dist_result.get("status") == 200:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Resumes Endpoints
    print_test_header("4. RESUMES ENDPOINTS")
    
    resumes_result = test_endpoint("GET", "/resumes/")
    if resumes_result.get("status") == 200:
        results["passed"] += 1
        resumes = resumes_result.get("data", [])
        print(f"[INFO] Found {len(resumes)} resumes in database")
        
        # Test resume upload
        print("\n[TEST] Testing resume upload...")
        test_resume_content = b"John Doe\nSenior Software Engineer\nPython, React, FastAPI"
        files_data = {"file": ("test_resume.txt", test_resume_content, "text/plain")}
        upload_result = test_endpoint("POST", "/resumes/upload", files=files_data)
        if upload_result.get("status") == 200:
            results["passed"] += 1
            print("[SUCCESS] Resume uploaded successfully")
        else:
            results["failed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Applications Endpoints
    print_test_header("5. APPLICATIONS ENDPOINTS")
    
    apps_result = test_endpoint("GET", "/applications/")
    if apps_result.get("status") == 200:
        results["passed"] += 1
        apps = apps_result.get("data", [])
        print(f"[INFO] Found {len(apps)} applications in database")
        
        # Test application submission (if we have jobs)
        if jobs_result.get("status") == 200:
            jobs = jobs_result.get("data", [])
            if jobs and len(jobs) > 0:
                test_job_id = jobs[0]["id"]
                print(f"\n[TEST] Testing application to job ID {test_job_id}...")
                apply_result = test_endpoint("POST", f"/applications/apply/{test_job_id}")
                if apply_result.get("status") in [200, 400]:  # 400 if already applied
                    results["passed"] += 1
                else:
                    results["failed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Projects Endpoint
    print_test_header("6. PROJECTS ENDPOINTS")
    
    project_search = test_endpoint("POST", "/projects/search", data=["Python", "React", "FastAPI"])
    if project_search.get("status") == 200:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    print(f"[PASSED] {results['passed']} tests")
    print(f"[FAILED] {results['failed']} tests")
    
    if results['errors']:
        print("\n[ERRORS]")
        for error in results['errors']:
            print(f"  - {error}")
    
    success_rate = (results['passed'] / (results['passed'] + results['failed']) * 100) if (results['passed'] + results['failed']) > 0 else 0
    print(f"\n[SUCCESS RATE] {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("\n[STATUS] PHASE 2 TESTING: PASSED ✓")
    else:
        print("\n[STATUS] PHASE 2 TESTING: NEEDS FIXES")
    
    print("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    print("\nStarting API tests...")
    print("Make sure the server is running on http://127.0.0.1:8000\n")
    
    try:
        results = run_all_tests()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Tests interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] Test suite failed: {e}")
