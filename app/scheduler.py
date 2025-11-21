"""Background job scheduler for continuous monitoring."""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
from app.tools.job_tools import scrape_jobs
from app.database import SessionLocal
from app.models import Job

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()


class JobMonitor:
    """Handles continuous job monitoring and scraping."""
    
    def __init__(self):
        self.enabled = False
        self.config = {
            "region": "Remote",
            "role": "Software Engineer",
            "platforms": ["LinkedIn", "Indeed"],
            "interval_minutes": 60
        }
    
    def configure(self, region: str, role: str, platforms: list, interval_minutes: int = 60):
        """Configure monitoring parameters."""
        self.config = {
            "region": region,
            "role": role,
            "platforms": platforms,
            "interval_minutes": interval_minutes
        }
        logger.info(f"Job monitor configured: {self.config}")
    
    def scrape_task(self):
        """Task that runs periodically to scrape jobs."""
        if not self.enabled:
            return
        
        try:
            logger.info(f"Running scheduled job scrape at {datetime.now()}")
            jobs = scrape_jobs(
                self.config["region"],
                self.config["role"],
                self.config["platforms"]
            )
            logger.info(f"Scraped {len(jobs)} jobs")
            
            # Store metrics
            db = SessionLocal()
            try:
                new_jobs = db.query(Job).filter(Job.scraped_at >= datetime.now()).count()
                logger.info(f"New jobs in last scrape: {new_jobs}")
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Scraping task error: {e}")
    
    def start(self):
        """Start continuous monitoring."""
        if self.enabled:
            logger.warning("Monitor already running")
            return
        
        self.enabled = True
        
        # Add job to scheduler
        scheduler.add_job(
            func=self.scrape_task,
            trigger=IntervalTrigger(minutes=self.config["interval_minutes"]),
            id="job_scraping",
            name="Continuous Job Scraping",
            replace_existing=True
        )
        
        logger.info(f"Job monitoring started (interval: {self.config['interval_minutes']}min)")
    
    def stop(self):
        """Stop continuous monitoring."""
        self.enabled = False
        if scheduler.get_job("job_scraping"):
            scheduler.remove_job("job_scraping")
        logger.info("Job monitoring stopped")
    
    def get_status(self):
        """Get current monitoring status."""
        job = scheduler.get_job("job_scraping")
        return {
            "enabled": self.enabled,
            "config": self.config,
            "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None,
            "scheduler_running": scheduler.running
        }


# Global monitor instance
job_monitor = JobMonitor()


def start_scheduler():
    """Start the background scheduler."""
    if not scheduler.running:
        scheduler.start()
        logger.info("Background scheduler started")


def stop_scheduler():
    """Stop the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background scheduler stopped")


def get_all_jobs():
    """Get all scheduled jobs."""
    return scheduler.get_jobs()
