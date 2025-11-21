"""
Test script for real job API integrations.
Run this to verify Adzuna, RemoteOK, and Indeed RSS feeds work.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.real_job_apis import (
    AdzunaAPI,
    RemoteOKAPI,
    IndeedRSSParser,
    JobAPIAggregator
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_adzuna():
    """Test Adzuna API"""
    print("\n" + "="*60)
    print("🔍 Testing Adzuna API")
    print("="*60)
    
    api = AdzunaAPI()
    
    if not api.app_id or not api.app_key:
        print("❌ Adzuna API credentials not found!")
        print("   Set ADZUNA_API_ID and ADZUNA_API_KEY in .env")
        return False
    
    try:
        jobs = api.search_jobs(
            country="us",
            query="python developer",
            location="New York",
            results_per_page=5
        )
        
        print(f"✅ Found {len(jobs)} jobs from Adzuna\n")
        
        for i, job in enumerate(jobs[:3], 1):
            print(f"{i}. {job.get('title')} at {job.get('company')}")
            print(f"   Location: {job.get('location')}")
            print(f"   URL: {job.get('url')[:60]}...")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Adzuna API Error: {e}")
        return False


def test_remoteok():
    """Test RemoteOK API"""
    print("\n" + "="*60)
    print("🌍 Testing RemoteOK API")
    print("="*60)
    
    api = RemoteOKAPI()
    
    try:
        jobs = api.search_jobs(search_query="python", limit=5)
        
        print(f"✅ Found {len(jobs)} remote jobs from RemoteOK\n")
        
        for i, job in enumerate(jobs[:3], 1):
            print(f"{i}. {job.get('title')} at {job.get('company')}")
            print(f"   Tags: {', '.join(job.get('tags', [])[:5])}")
            print(f"   URL: {job.get('url')}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ RemoteOK API Error: {e}")
        return False


def test_indeed_rss():
    """Test Indeed RSS Parser"""
    print("\n" + "="*60)
    print("📰 Testing Indeed RSS Feed")
    print("="*60)
    
    parser = IndeedRSSParser()
    
    try:
        jobs = parser.search_jobs(
            query="backend engineer",
            location="San Francisco",
            limit=5
        )
        
        print(f"✅ Found {len(jobs)} jobs from Indeed RSS\n")
        
        for i, job in enumerate(jobs[:3], 1):
            print(f"{i}. {job.get('title')} at {job.get('company')}")
            print(f"   URL: {job.get('url')[:60]}...")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Indeed RSS Error: {e}")
        return False


def test_aggregator():
    """Test JobAPIAggregator"""
    print("\n" + "="*60)
    print("🚀 Testing Job API Aggregator (All Platforms)")
    print("="*60)
    
    aggregator = JobAPIAggregator()
    
    try:
        jobs = aggregator.search_all_platforms(
            query="software engineer",
            location="Remote",
            platforms=["adzuna", "remoteok", "indeed"],
            limit_per_platform=3
        )
        
        print(f"\n✅ Total jobs found: {len(jobs)}")
        
        # Group by source
        by_source = {}
        for job in jobs:
            source = job.get('source', 'Unknown')
            by_source[source] = by_source.get(source, 0) + 1
        
        print("\nBreakdown by source:")
        for source, count in by_source.items():
            print(f"  - {source}: {count} jobs")
        
        print("\nSample jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job.get('title')} at {job.get('company')}")
            print(f"   Source: {job.get('source')}")
            print(f"   Location: {job.get('location')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Aggregator Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🧪 " * 20)
    print("REAL JOB API INTEGRATION TESTS")
    print("🧪 " * 20)
    
    results = {
        "Adzuna": test_adzuna(),
        "RemoteOK": test_remoteok(),
        "Indeed RSS": test_indeed_rss(),
        "Aggregator": test_aggregator()
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your job APIs are working!\n")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check configuration above.\n")
        return 1


if __name__ == "__main__":
    exit(main())
