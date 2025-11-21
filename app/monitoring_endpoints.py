# --- Monitoring & Scheduler Endpoints ---

@app.post("/monitor/configure")
def configure_monitoring(request: MonitorConfigRequest):
    """Configure continuous job monitoring parameters."""
    job_monitor.configure(
        region=request.region,
        role=request.role,
        platforms=request.platforms,
        interval_minutes=request.interval_minutes
    )
    return {
        "status": "configured",
        "config": job_monitor.config
    }

@app.post("/monitor/start")
def start_monitoring():
    """Start continuous job monitoring."""
    job_monitor.start()
    return {
        "status": "started",
        "message": f"Monitoring activated. Jobs will be scraped every {job_monitor.config['interval_minutes']} minutes"
    }

@app.post("/monitor/stop")
def stop_monitoring():
    """Stop continuous job monitoring."""
    job_monitor.stop()
    return {
        "status": "stopped",
        "message": "Monitoring deactivated"
    }

@app.get("/monitor/status")
def get_monitoring_status():
    """Get current monitoring status."""
    return job_monitor.get_status()

# --- Notification Endpoints ---

@app.post("/notifications/test")
def test_notification(request: NotificationTestRequest):
    """Send a test notification email."""
    test_job = {
        "title": "Test Job - Senior Software Engineer",
        "company": "Test Company Inc.",
        "location": "Remote",
        "match_score": 95,
        "url": "http://127.0.0.1:8000",
        "raw_description": "This is a test job notification to verify email configuration.",
        "parsed_data": {
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "seniority": "Senior"
        }
    }
    
    success = notification_service.notify_high_match_job(test_job)
    
    return {
        "success": success,
        "message": "Test email sent" if success else "Email not configured. Check NOTIFICATIONS_ENABLED and SMTP settings in environment."
    }

@app.get("/notifications/config")
def get_notification_config():
    """Get current notification configuration."""
    return {
        "enabled": notification_service.enabled,
        "smtp_configured": bool(notification_service.sender_email and notification_service.sender_password),
        "recipient": notification_service.recipient_email if notification_service.enabled else "Not configured"
    }
