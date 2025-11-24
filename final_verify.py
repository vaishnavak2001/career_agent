"""Final verification script for Career Agent."""
import sys
import os

def check_imports():
    print("[CHECK] Verifying imports...")
    try:
        from app.main import app
        print("  [OK] app.main imported")
        
        from app.auth.jwt import create_access_token
        print("  [OK] app.auth.jwt imported")
        
        from app.agent.orchestrator import career_agent
        print("  [OK] app.agent.orchestrator imported")
        
        from app.scrapers.playwright_scraper import scraper
        print("  [OK] app.scrapers.playwright_scraper imported")
        
        from app.services.interview_prep import interview_service
        print("  [OK] app.services.interview_prep imported")
        
        from app.api.endpoints import auth, interview
        print("  [OK] New endpoints imported")
        
        print("[SUCCESS] All modules importable.")
        return True
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if check_imports():
        sys.exit(0)
    else:
        sys.exit(1)
