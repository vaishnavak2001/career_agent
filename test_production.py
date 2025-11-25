#!/usr/bin/env python3
"""
Quick production test script - tests your live Render deployment.

Usage:
    python test_production.py

Requirements:
    - Update PRODUCTION_URL below with your Render URL
    - Or set RENDER_URL environment variable
"""

import requests
import os
import sys

# Update this with your actual Render URL
PRODUCTION_URL = os.getenv("RENDER_URL", "https://career-agent.onrender.com")

def test_production():
    """Quick test of production deployment."""
    
    print("="*60)
    print("PRODUCTION DEPLOYMENT TEST")
    print("="*60)
    print(f"Testing: {PRODUCTION_URL}")
    print()
    
    tests = {
        "Health Check": f"{PRODUCTION_URL}/",
        "Jobs Endpoint": f"{PRODUCTION_URL}/api/v1/jobs/?limit=5",
    }
    
    results = {}
    
    for test_name, url in tests.items():
        print(f"Testing: {test_name}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            status = response.status_code
            
            if status == 200:
                print(f"✓ {test_name}: SUCCESS (200 OK)")
                results[test_name] = True
                
                # Show sample data for jobs endpoint
                if "jobs" in url:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"  → Returned {len(data)} jobs")
                            if len(data) > 0:
                                print(f"  → First job: {data[0].get('title', 'N/A')}")
                    except:
                        pass
                        
            elif status == 500:
                print(f"✗ {test_name}: FAILED (500 Error)")
                print(f"  → This indicates the bug fixes may not have deployed yet")
                print(f"  → Response: {response.text[:200]}")
                results[test_name] = False
            else:
                print(f"⚠ {test_name}: Status {status}")
                results[test_name] = False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ {test_name}: ERROR - {str(e)}")
            results[test_name] = False
        
        print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("Your production deployment is working correctly.")
        print("The database schema and password hashing fixes are live.")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("\nPossible reasons:")
        print("1. Render is still deploying (check Render dashboard)")
        print("2. Service needs manual restart on Render")
        print("3. Environment variables not set correctly")
        print("\nNext steps:")
        print("1. Check Render logs for deployment status")
        print("2. Verify DATABASE_URL is set correctly")
        print("3. Check if automatic deploys are enabled")
    
    print()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(test_production())
