from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Job, Application, Project

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get aggregated dashboard statistics.
    """
    total_scraped = db.query(Job).count()
    total_applied = db.query(Application).count()
    scams_detected = db.query(Job).filter(Job.is_scam == True).count()
    
    # Mock interviews for now as we don't track them yet
    interviews = 0
    
    return {
        "jobs_scraped": total_scraped,
        "applications_sent": total_applied,
        "interviews": interviews,
        "scams_blocked": scams_detected
    }

@router.get("/match-distribution")
def get_match_distribution(db: Session = Depends(get_db)):
    """
    Get distribution of match scores.
    """
    # Group by score ranges: 0-20, 21-40, 41-60, 61-80, 81-100
    distribution = {
        "0-20": 0,
        "21-40": 0,
        "41-60": 0,
        "61-80": 0,
        "81-100": 0
    }
    
    scores = db.query(Job.match_score).filter(Job.match_score != None).all()
    
    for (score,) in scores:
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
