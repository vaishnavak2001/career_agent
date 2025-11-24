"""Background job scheduler for continuous monitoring."""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import logging
from typing import Dict, Any

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
        logger.info(f"[SCHEDULER] Job monitor configured: {self.config}")
    
    def scrape_task(self):
        """Task that runs periodically to scrape jobs."""
        if not self.enabled:
            return
        
        try:
            from app.database import get_db_session
            from app.models import Job
            
            logger.info(f"[SCHEDULER] Running scheduled job scrape at {datetime.now()}")
            
            # Import scraping service
            try:
                from app.services.adzuna import adzuna_service
                import asyncio
                
                # Run async function in sync context
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                jobs = loop.run_until_complete(
                    adzuna_service.search_jobs(
                        self.config["role"],
                        self.config["region"]
                    )
                )
                loop.close()
                
                logger.info(f"[SCHEDULER] Found {len(jobs) if jobs else 0} jobs from Adzuna")
                
                # Save to database
                if jobs:
                    db = get_db_session()
                    try:
                        saved_count = 0
                        for job_data in jobs:
                            # Check for duplicates
                            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
                            if not existing:
                                job = Job(
                                    title=job_data["title"],
                                    company=job_data["company"],
                                    location=job_data["location"],
                                    url=job_data["url"],
                                    source=job_data["source"],
                                    raw_text=job_data.get("description"),
                                    match_score=0.0  # TODO: Calculate match score
                                )
                                db.add(job)
                                saved_count += 1
                        
                        db.commit()
                        logger.info(f"[SCHEDULER] Saved {saved_count} new jobs to database")
                    finally:
                        db.close()
                        
            except Exception as e:
                logger.error(f"[SCHEDULER] Scraping service error: {e}")
                
        except Exception as e:
            logger.error(f"[SCHEDULER] Scraping task error: {e}")
    
    def start(self):
        """Start continuous monitoring."""
        if self.enabled:
            logger.warning("[SCHEDULER] Monitor already running")
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
        
        logger.info(f"[SCHEDULER] Job monitoring started (interval: {self.config['interval_minutes']}min)")
    
    def stop(self):
        """Stop continuous monitoring."""
        self.enabled = False
        if scheduler.get_job("job_scraping"):
            scheduler.remove_job("job_scraping")
        logger.info("[SCHEDULER] Job monitoring stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        job = scheduler.get_job("job_scraping")
        return {
            "enabled": self.enabled,
            "config": self.config,
            "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None,
            "scheduler_running": scheduler.running
        }


def cleanup_old_jobs():
    """Clean up jobs older than 30 days."""
    try:
        from app.database import get_db_session
        from app.models import Job
        
        logger.info("[SCHEDULER] Running cleanup task...")
        db = get_db_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            deleted = db.query(Job).filter(Job.scraped_at < cutoff_date).delete()
            db.commit()
            logger.info(f"[SCHEDULER] Deleted {deleted} old jobs")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"[SCHEDULER] Cleanup task error: {e}")


def daily_analytics_aggregation():
    """Aggregate daily analytics."""
    try:
        from app.database import get_db_session
        from app.models import DailyMetric, Job, Application
        from datetime import date
        
        logger.info("[SCHEDULER] Running daily analytics aggregation...")
        db = get_db_session()
        try:
            today = date.today()
            
            # Check if already aggregated
            existing = db.query(DailyMetric).filter(DailyMetric.date == today).first()
            if existing:
                logger.info("[SCHEDULER] Analytics already aggregated for today")
                return
            
            # Calculate metrics
            jobs_scraped = db.query(Job).filter(Job.scraped_at >= datetime.combine(today, datetime.min.time())).count()
            jobs_matched = db.query(Job).filter(Job.match_score >= 70).count()
            applications = db.query(Application).filter(Application.applied_at >= datetime.combine(today, datetime.min.time())).count()
            scams = db.query(Job).filter(Job.is_scam == True).count()
            
            # Save metrics
            metric = DailyMetric(
                date=today,
                jobs_scraped=jobs_scraped,
                jobs_matched=jobs_matched,
                applications_sent=applications,
                scams_detected=scams
            )
            db.add(metric)
            db.commit()
            
            logger.info(f"[SCHEDULER] Daily analytics saved: {jobs_scraped} jobs, {applications} applications")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"[SCHEDULER] Analytics aggregation error: {e}")


# Global monitor instance
job_monitor = JobMonitor()


def start_scheduler():
    """Start the background scheduler with all scheduled tasks."""
    if scheduler.running:
        logger.warning("[SCHEDULER] Scheduler already running")
        return
    
    # Add cleanup job (daily at 2 AM)
    scheduler.add_job(
        func=cleanup_old_jobs,
        trigger=CronTrigger(hour=2, minute=0),
        id="cleanup_old_jobs",
        name="Daily Cleanup of Old Jobs",
        replace_existing=True
    )
    
    # Add analytics aggregation (daily at 23:59)
    scheduler.add_job(
        func=daily_analytics_aggregation,
        trigger=CronTrigger(hour=23, minute=59),
        id="daily_analytics",
        name="Daily Analytics Aggregation",
        replace_existing=True
    )
    
    # Start scheduler
    scheduler.start()
    logger.info("[SCHEDULER] Background scheduler started with all jobs")
    logger.info(f"[SCHEDULER] Scheduled jobs: {len(scheduler.get_jobs())}")


def stop_scheduler():
    """Stop the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("[SCHEDULER] Background scheduler stopped")


def get_all_jobs():
    """Get all scheduled jobs."""
    return [
        {
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger)
        }
        for job in scheduler.get_jobs()
    ]


def get_scheduler_status() -> Dict[str, Any]:
    """Get comprehensive scheduler status."""
    return {
        "running": scheduler.running,
        "jobs_count": len(scheduler.get_jobs()),
        "jobs": get_all_jobs(),
        "job_monitor": job_monitor.get_status()
    }
