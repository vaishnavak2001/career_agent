"""Analytics and dashboard metrics tools."""
from typing import Dict, Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Job, Application, Project
from app.database import SessionLocal
from datetime import datetime, timedelta


def dashboard_metrics() -> Dict[str, Any]:
    """
    Generates comprehensive dashboard metrics.
    """
    db = SessionLocal()
    try:
        # Total jobs scraped
        total_jobs = db.query(Job).count()
        
        # Jobs with high match scores (>= 70)
        matched_jobs = db.query(Job).filter(Job.match_score >= 70).count()
        
        # Total applications submitted
        total_applied = db.query(Application).count()
        
        # Scam jobs detected
        scams_detected = db.query(Job).filter(Job.is_scam == True).count()
        
        # Duplicates avoided (jobs with same company+title)
        # This is tricky to calculate, so we'll estimate
        duplicates_avoided = total_jobs - db.query(Job.company, Job.title).distinct().count()
        
        # Average match score
        avg_match = db.query(func.avg(Job.match_score)).scalar() or 0
        
        # Most requested skills
        skills_count = {}
        jobs_with_parsed = db.query(Job).filter(Job.parsed_data.isnot(None)).all()
        for job in jobs_with_parsed:
            if job.parsed_data and "skills" in job.parsed_data:
                for skill in job.parsed_data["skills"]:
                    skills_count[skill] = skills_count.get(skill, 0) + 1
        
        top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Company-wise stats
        company_stats = db.query(
            Job.company,
            func.count(Job.id).label('job_count'),
            func.avg(Job.match_score).label('avg_match')
        ).group_by(Job.company).all()
        
        company_breakdown = [
            {"company": stat.company, "jobs": stat.job_count, "avg_match": round(stat.avg_match or 0, 2)}
            for stat in company_stats
        ]
        
        # Application success rate (mock - would need actual tracking)
        success_rate = 0.15  # 15% mock success rate
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_jobs = db.query(Job).filter(Job.scraped_at >= week_ago).count()
        recent_applications = db.query(Application).filter(Application.submitted_at >= week_ago).count()
        
        # Projects added
        total_projects = db.query(Project).count()
        
        return {
            "overview": {
                "total_jobs_scraped": total_jobs,
                "matched_jobs": matched_jobs,
                "total_applied": total_applied,
                "duplicates_avoided": duplicates_avoided,
                "scams_detected": scams_detected,
                "projects_added": total_projects
            },
            "performance": {
                "average_match_score": round(avg_match, 2),
                "application_success_rate": success_rate,
                "match_rate": round((matched_jobs / total_jobs * 100) if total_jobs > 0 else 0, 2)
            },
            "trends": {
                "recent_jobs_7d": recent_jobs,
                "recent_applications_7d": recent_applications
            },
            "top_skills": [{"skill": skill, "count": count} for skill, count in top_skills],
            "company_breakdown": company_breakdown[:10]
        }
    finally:
        db.close()


def get_match_score_distribution() -> Dict[str, int]:
    """
    Returns distribution of match scores in buckets.
    """
    db = SessionLocal()
    try:
        jobs = db.query(Job.match_score).all()
        
        distribution = {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0
        }
        
        for job in jobs:
            score = job.match_score or 0
            if score <= 20:
                distribution["0-20"] += 1
            elif score <= 40:
                distribution["21-40"] += 1
            elif score <= 60:
                distribution["41-60"] += 1
            elif score <= 80:
                distribution["61-80"] += 1
            else:
                distribution["81-100"] += 1
        
        return distribution
    finally:
        db.close()


def get_application_timeline() -> List[Dict[str, Any]]:
    """
    Returns timeline of applications over time.
    """
    db = SessionLocal()
    try:
        applications = db.query(Application).order_by(Application.submitted_at).all()
        
        timeline = []
        for app in applications:
            job = db.query(Job).filter(Job.id == app.job_id).first()
            timeline.append({
                "date": app.submitted_at.isoformat() if app.submitted_at else None,
                "company": job.company if job else "Unknown",
                "title": job.title if job else "Unknown",
                "status": app.status
            })
        
        return timeline
    finally:
        db.close()
