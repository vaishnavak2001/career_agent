import httpx
import logging
from typing import List, Dict, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class AdzunaService:
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def __init__(self):
        self.app_id = settings.ADZUNA_API_ID
        self.app_key = settings.ADZUNA_API_KEY

    async def search_jobs(self, role: str, location: str, country: str = "us", results_per_page: int = 20) -> List[Dict]:
        """
        Search for jobs using the Adzuna API.
        """
        if not self.app_id or not self.app_key:
            logger.warning("Adzuna API credentials not found. Skipping Adzuna search.")
            return []

        url = f"{self.BASE_URL}/{country}/search/1"
        
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": results_per_page,
            "what": role,
            "where": location,
            "content-type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                results = data.get("results", [])
                return self._normalize_results(results)
            except Exception as e:
                logger.error(f"Error searching Adzuna: {e}")
                return []

    def _normalize_results(self, results: List[Dict]) -> List[Dict]:
        """
        Convert Adzuna results to our internal Job format.
        """
        normalized = []
        for item in results:
            try:
                job = {
                    "title": item.get("title"),
                    "company": item.get("company", {}).get("display_name"),
                    "location": item.get("location", {}).get("display_name"),
                    "description": item.get("description"),
                    "url": item.get("redirect_url"),
                    "source": "Adzuna",
                    "posted_date": item.get("created"),
                    "salary_min": item.get("salary_min"),
                    "salary_max": item.get("salary_max"),
                    "contract_type": item.get("contract_type")
                }
                normalized.append(job)
            except Exception as e:
                logger.warning(f"Error normalizing job item: {e}")
                continue
        return normalized

adzuna_service = AdzunaService()
