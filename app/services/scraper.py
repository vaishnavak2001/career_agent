import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class JobScraper:
    def __init__(self):
        self.headless = True

    async def scrape_indeed(self, role: str, region: str) -> List[Dict]:
        """
        Scrape jobs from Indeed (simulated/simplified for now).
        """
        jobs = []
        url = f"https://www.indeed.com/jobs?q={role}&l={region}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                # Note: Indeed has heavy anti-bot. This is a basic attempt.
                # In a real production system, you'd use a scraping API or more advanced evasion.
                await page.goto(url, timeout=30000)
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # This selector is subject to change by Indeed
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards:
                    try:
                        title_elem = card.select_one('h2.jobTitle span')
                        company_elem = card.select_one('[data-testid="company-name"]')
                        location_elem = card.select_one('[data-testid="text-location"]')
                        link_elem = card.select_one('a.jcs-JobTitle')
                        
                        if title_elem and company_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip()
                            location = location_elem.text.strip() if location_elem else region
                            link = "https://www.indeed.com" + link_elem['href'] if link_elem else ""
                            
                            jobs.append({
                                "title": title,
                                "company": company,
                                "location": location,
                                "url": link,
                                "source": "indeed"
                            })
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error scraping Indeed: {e}")
                # Fallback mock data for demo/testing if scraping fails
                if not jobs:
                    print("Using mock data due to scraping error")
                    jobs = [
                        {
                            "title": "Senior Software Engineer",
                            "company": "Tech Corp (Mock)",
                            "location": region,
                            "url": "https://example.com/job1",
                            "source": "mock"
                        },
                        {
                            "title": "Python Developer",
                            "company": "Startup Inc (Mock)",
                            "location": "Remote",
                            "url": "https://example.com/job2",
                            "source": "mock"
                        }
                    ]
            finally:
                await browser.close()
                
        return jobs

    async def scrape_jobs(self, role: str, region: str, platforms: List[str]) -> List[Dict]:
        all_jobs = []
        if "indeed" in platforms:
            jobs = await self.scrape_indeed(role, region)
            all_jobs.extend(jobs)
        
        # Add other platforms here
        
        return all_jobs

scraper_service = JobScraper()
