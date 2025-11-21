"""Real-world job API integrations for Adzuna, RemoteOK, and Indeed RSS."""
import requests
import feedparser
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
import os
from sqlalchemy.orm import Session
from app.models import Job
from app.database import SessionLocal
import logging

logger = logging.getLogger(__name__)


class AdzunaAPI:
    """
    Adzuna Job Search API Integration
    Sign up at: https://developer.adzuna.com/
    Free tier: 5000 calls/month
    """
    
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"
    
    def __init__(self, app_id: str = None, app_key: str = None):
        self.app_id = app_id or os.getenv("ADZUNA_API_ID")
        self.app_key = app_key or os.getenv("ADZUNA_API_KEY")
        
        if not self.app_id or not self.app_key:
            logger.warning("Adzuna API credentials not found. Set ADZUNA_API_ID and ADZUNA_API_KEY in .env")
    
    def search_jobs(
        self,
        country: str = "us",
        query: str = "python developer",
        location: str = "New York",
        results_per_page: int = 20,
        page: int = 1,
        sort_by: str = "date"  # Options: date, relevance, salary
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs using Adzuna API
        
        Args:
            country: Two-letter country code (us, uk, ca, au, etc.)
            query: Search keywords (e.g., "python developer")
            location: City or region name
            results_per_page: Number of results (max 50)
            page: Page number for pagination
            sort_by: Sort order (date, relevance, salary)
        
        Returns:
            List of job dictionaries
        """
        if not self.app_id or not self.app_key:
            logger.error("Cannot search Adzuna: Missing API credentials")
            return []
        
        url = f"{self.BASE_URL}/{country}/search/{page}"
        
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": results_per_page,
            "what": query,
            "where": location,
            "sort_by": sort_by,
            "content-type": "application/json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for result in data.get("results", []):
                job = self._parse_adzuna_job(result)
                jobs.append(job)
            
            logger.info(f"Adzuna: Found {len(jobs)} jobs for '{query}' in {location}")
            return jobs
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Adzuna API error: {e}")
            return []
    
    def _parse_adzuna_job(self, result: Dict) -> Dict[str, Any]:
        """Parse Adzuna API response into standardized format"""
        return {
            "url": result.get("redirect_url"),
            "title": result.get("title"),
            "company": result.get("company", {}).get("display_name", "Unknown"),
            "location": result.get("location", {}).get("display_name", "Unknown"),
            "posted_date": datetime.fromisoformat(result.get("created").replace("Z", "+00:00")) if result.get("created") else datetime.now(),
            "raw_description": result.get("description", ""),
            "salary_min": result.get("salary_min"),
            "salary_max": result.get("salary_max"),
            "contract_type": result.get("contract_type"),
            "category": result.get("category", {}).get("label"),
            "source": "Adzuna"
        }


class RemoteOKAPI:
    """
    RemoteOK Job Board Integration
    Free JSON API - no authentication required
    Documentation: https://remoteok.com/api
    """
    
    BASE_URL = "https://remoteok.com/api"
    
    def search_jobs(
        self,
        search_query: str = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetch remote jobs from RemoteOK
        
        Args:
            search_query: Optional search term (filters after fetching)
            limit: Max number of jobs to return
        
        Returns:
            List of job dictionaries
        """
        headers = {
            "User-Agent": "Career-Agent-Bot/1.0 (https://github.com/yourusername/career-agent)"
        }
        
        try:
            # RemoteOK requires a respectful user agent
            response = requests.get(self.BASE_URL, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # First item is metadata, skip it
            jobs_data = data[1:] if isinstance(data, list) and len(data) > 1 else []
            
            jobs = []
            for result in jobs_data[:limit]:
                # Filter by search query if provided
                if search_query:
                    query_lower = search_query.lower()
                    position = result.get("position", "").lower()
                    tags = " ".join(result.get("tags", [])).lower()
                    
                    if query_lower not in position and query_lower not in tags:
                        continue
                
                job = self._parse_remoteok_job(result)
                jobs.append(job)
            
            logger.info(f"RemoteOK: Found {len(jobs)} remote jobs")
            return jobs
            
        except requests.exceptions.RequestException as e:
            logger.error(f"RemoteOK API error: {e}")
            return []
    
    def _parse_remoteok_job(self, result: Dict) -> Dict[str, Any]:
        """Parse RemoteOK API response into standardized format"""
        try:
            # Handle different date formats (int timestamp or string)
            date_val = result.get("date")
            if isinstance(date_val, (int, float)):
                posted_date = datetime.fromtimestamp(date_val)
            elif isinstance(date_val, str):
                posted_date = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
            else:
                posted_date = datetime.now()
        except Exception:
            posted_date = datetime.now()

        return {
            "url": result.get("url") or f"https://remoteok.com/remote-jobs/{result.get('id')}",
            "title": result.get("position"),
            "company": result.get("company"),
            "location": "Remote",
            "posted_date": posted_date,
            "raw_description": result.get("description", ""),
            "salary_min": result.get("salary_min"),
            "salary_max": result.get("salary_max"),
            "tags": result.get("tags", []),
            "apply_url": result.get("apply_url"),
            "source": "RemoteOK"
        }


class IndeedRSSParser:
    """
    Indeed RSS Feed Parser
    Legal and respectful way to get Indeed jobs
    Example: https://www.indeed.com/rss?q=python+developer&l=New+York
    """
    
    BASE_URL = "https://www.indeed.com/rss"
    
    def search_jobs(
        self,
        query: str = "python developer",
        location: str = "New York",
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Parse Indeed RSS feed for jobs
        
        Args:
            query: Job search keywords
            location: Location name
            limit: Max results
        
        Returns:
            List of job dictionaries
        """
        params = {
            "q": query,
            "l": location
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            jobs = []
            for entry in feed.entries[:limit]:
                job = self._parse_indeed_entry(entry)
                jobs.append(job)
            
            logger.info(f"Indeed RSS: Found {len(jobs)} jobs for '{query}' in {location}")
            return jobs
            
        except Exception as e:
            logger.error(f"Indeed RSS error: {e}")
            return []
    
    def _parse_indeed_entry(self, entry) -> Dict[str, Any]:
        """Parse RSS entry into standardized format"""
        # Extract company from title (format: "Job Title - Company Name")
        title_parts = entry.title.split(" - ")
        job_title = title_parts[0] if len(title_parts) > 0 else entry.title
        company = title_parts[1] if len(title_parts) > 1 else "Unknown"
        
        return {
            "url": entry.link,
            "title": job_title,
            "company": company,
            "location": entry.get("summary", "Unknown"),
            "posted_date": datetime(*entry.published_parsed[:6]) if hasattr(entry, "published_parsed") else datetime.now(),
            "raw_description": entry.get("summary", ""),
            "source": "Indeed"
        }


class JobAPIAggregator:
    """
    Aggregates jobs from multiple sources
    """
    
    def __init__(self):
        self.adzuna = AdzunaAPI()
        self.remoteok = RemoteOKAPI()
        self.indeed_rss = IndeedRSSParser()
    
    def search_all_platforms(
        self,
        query: str = "python developer",
        location: str = "New York",
        platforms: List[str] = None,
        limit_per_platform: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search across all available platforms
        
        Args:
            query: Job search keywords
            location: Location name
            platforms: List of platforms to search (None = all)
            limit_per_platform: Max results from each platform
        
        Returns:
            Combined list of jobs from all platforms
        """
        all_jobs = []
        
        if platforms is None:
            platforms = ["adzuna", "remoteok", "indeed"]
        
        # Adzuna
        if "adzuna" in [p.lower() for p in platforms]:
            try:
                adzuna_jobs = self.adzuna.search_jobs(
                    query=query,
                    location=location,
                    results_per_page=limit_per_platform
                )
                all_jobs.extend(adzuna_jobs)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Adzuna search failed: {e}")
        
        # RemoteOK
        if "remoteok" in [p.lower() for p in platforms]:
            try:
                remote_jobs = self.remoteok.search_jobs(
                    search_query=query,
                    limit=limit_per_platform
                )
                all_jobs.extend(remote_jobs)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"RemoteOK search failed: {e}")
        
        # Indeed RSS
        if "indeed" in [p.lower() for p in platforms]:
            try:
                indeed_jobs = self.indeed_rss.search_jobs(
                    query=query,
                    location=location,
                    limit=limit_per_platform
                )
                all_jobs.extend(indeed_jobs)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Indeed RSS search failed: {e}")
        
        logger.info(f"Total jobs found across all platforms: {len(all_jobs)}")
        return all_jobs
    
    def save_jobs_to_db(self, jobs: List[Dict[str, Any]], db: Session = None) -> int:
        """
        Save jobs to database, avoiding duplicates
        
        Returns:
            Number of new jobs saved
        """
        if db is None:
            db = SessionLocal()
            close_db = True
        else:
            close_db = False
        
        saved_count = 0
        
        try:
            for job_data in jobs:
                # Check for duplicates
                existing = db.query(Job).filter(Job.url == job_data["url"]).first()
                
                if not existing:
                    # Create new job entry
                    job = Job(
                        **job_data,
                        status="scraped"
                    )
                    db.add(job)
                    saved_count += 1
            
            db.commit()
            logger.info(f"Saved {saved_count} new jobs to database")
            
        except Exception as e:
            logger.error(f"Database save error: {e}")
            db.rollback()
        
        finally:
            if close_db:
                db.close()
        
        return saved_count


# Convenience function for easy import
def search_real_jobs(
    query: str = "python developer",
    location: str = "New York",
    platforms: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Quick function to search real job boards
    
    Usage:
        jobs = search_real_jobs("Backend Engineer", "San Francisco")
    """
    aggregator = JobAPIAggregator()
    return aggregator.search_all_platforms(query, location, platforms)
