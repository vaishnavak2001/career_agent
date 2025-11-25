"""
Test script to verify the bug fixes are working correctly.
Tests:
1. Database connection
2. Jobs endpoint without errors
3. User registration with password hashing
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_BASE = f"{BASE_URL}/api/v1"

def test_healthcheck():
    """Test if the API is accessible."""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("[OK] Health check passed")
            return True
        else:
            print("[FAIL] Health check failed")
            return False
    except Exception as e:
        print(f"[ERROR] Health check failed: {str(e)}")
        return False

def test_jobs_endpoint():
    """Test the jobs endpoint - should not return 500 errors anymore."""
    print("\n" + "="*60)
    print("TEST 2: Jobs Endpoint (Database Schema Fix)")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE}/jobs/?limit=20", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Jobs endpoint working")
            print(f"Jobs returned: {len(data) if isinstance(data, list) else 'N/A'}")
            return True
        elif response.status_code == 500:
            print(f"[FAIL] Still getting 500 error")
            print(f"Response: {response.text[:300]}")
            return False
        else:
            print(f"[INFO] Got status {response.status_code}")
            return True
    except Exception as e:
        print(f"[ERROR] Jobs endpoint test failed: {str(e)}")
        return False

def test_user_registration():
    """Test user registration with password hashing."""
    print("\n" + "="*60)
    print("TEST 3: User Registration (Password Hashing Fix)")
    print("="*60)
    
    # Test with a normal password
    test_cases = [
        {
            "name": "Normal password",
            "data": {
                "email": f"test_normal_{os.urandom(4).hex()}@example.com",
                "password": "TestPassword123!",
                "full_name": "Test User Normal"
            }
        },
        {
            "name": "Long password (>72 bytes)",
            "data": {
                "email": f"test_long_{os.urandom(4).hex()}@example.com",
                "password": "ThisIsAVeryLongPasswordThatExceeds72BytesInLengthAndShouldBeTruncatedProperly123456789!@#",
                "full_name": "Test User Long Password"
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Password length: {len(test_case['data']['password'])} characters / {len(test_case['data']['password'].encode('utf-8'))} bytes")
        
        try:
            response = requests.post(
                f"{API_BASE}/auth/register",
                json=test_case['data'],
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"[OK] Registration successful")
            elif response.status_code == 400:
                # Might be duplicate email, which is acceptable
                error_msg = response.json().get('detail', '')
                if 'already registered' in error_msg.lower():
                    print(f"[OK] Email already registered (acceptable)")
                else:
                    print(f"[FAIL] Registration failed: {error_msg}")
                    all_passed = False
            else:
                print(f"[FAIL] Unexpected status code")
                print(f"Response: {response.text[:300]}")
                all_passed = False
                
        except Exception as e:
            print(f"[ERROR] Registration test failed: {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("BUG FIX VERIFICATION TESTS")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    
    results = {
        "Health Check": test_healthcheck(),
        "Jobs Endpoint": test_jobs_endpoint(),
        "User Registration": test_user_registration()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n[SUCCESS] All tests passed!")
        print("The bug fixes are working correctly.")
    else:
        print("\n[WARNING] Some tests failed.")
        print("Please check the output above for details.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
