"""Playwright-based scraper for job platforms."""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Page, Browser

logger = logging.getLogger(__name__)

class PlaywrightScraper:
    """Scraper using Playwright for dynamic content."""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.playwright = None

    async def start(self):
        """Start the browser session."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        logger.info("Playwright browser started")

    async def stop(self):
        """Stop the browser session."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Playwright browser stopped")

    async def scrape_linkedin(self, search_term: str, location: str) -> List[Dict[str, Any]]:
        """Scrape LinkedIn jobs (public view)."""
        if not self.browser:
            await self.start()
            
        page = await self.browser.new_page()
        jobs = []
        
        try:
            # Construct URL
            url = f"https://www.linkedin.com/jobs/search?keywords={search_term}&location={location}"
            logger.info(f"Navigating to: {url}")
            
            await page.goto(url, wait_until="networkidle")
            
            # Scroll to load more jobs
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)
            
            # Extract job cards
            job_cards = await page.query_selector_all(".base-card")
            
            for card in job_cards[:10]:  # Limit to 10 for demo
                try:
                    title_el = await card.query_selector(".base-search-card__title")
                    company_el = await card.query_selector(".base-search-card__subtitle")
                    location_el = await card.query_selector(".job-search-card__location")
                    link_el = await card.query_selector(".base-card__full-link")
                    
                    if title_el and company_el and link_el:
                        title = await title_el.inner_text()
                        company = await company_el.inner_text()
                        loc = await location_el.inner_text() if location_el else location
                        link = await link_el.get_attribute("href")
                        
                        jobs.append({
                            "title": title.strip(),
                            "company": company.strip(),
                            "location": loc.strip(),
                            "url": link,
                            "source": "linkedin",
                            "description": "Description not fetched in list view" 
                        })
                except Exception as e:
                    logger.warning(f"Error extracting job card: {e}")
                    
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {e}")
        finally:
            await page.close()
            
        return jobs

    async def scrape_indeed(self, search_term: str, location: str) -> List[Dict[str, Any]]:
        """Scrape Indeed jobs."""
        if not self.browser:
            await self.start()
            
        page = await self.browser.new_page()
        jobs = []
        
        try:
            url = f"https://www.indeed.com/jobs?q={search_term}&l={location}"
            logger.info(f"Navigating to: {url}")
            
            await page.goto(url, wait_until="domcontentloaded")
            
            # Handle potential popups or captchas here (simplified)
            
            job_cards = await page.query_selector_all(".job_seen_beacon")
            
            for card in job_cards[:10]:
                try:
                    title_el = await card.query_selector("h2.jobTitle span")
                    company_el = await card.query_selector("[data-testid='company-name']")
                    location_el = await card.query_selector("[data-testid='text-location']")
                    link_el = await card.query_selector("a.jcs-JobTitle")
                    
                    if title_el and link_el:
                        title = await title_el.inner_text()
                        company = await company_el.inner_text() if company_el else "Unknown"
                        loc = await location_el.inner_text() if location_el else location
                        link_suffix = await link_el.get_attribute("href")
                        link = f"https://www.indeed.com{link_suffix}"
                        
                        jobs.append({
                            "title": title.strip(),
                            "company": company.strip(),
                            "location": loc.strip(),
                            "url": link,
                            "source": "indeed",
                            "description": "Description not fetched in list view"
                        })
                except Exception as e:
                    logger.warning(f"Error extracting Indeed card: {e}")
                    
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")
        finally:
            await page.close()
            
        return jobs

# Global instance
scraper = PlaywrightScraper()
