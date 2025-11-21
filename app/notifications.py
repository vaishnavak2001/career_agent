"""Email notification system for job alerts."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Handles email notifications for job alerts."""
    
    def __init__(self):
        self.enabled = os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", "")
    
    def send_email(self, subject: str, body: str, html: bool = True):
        """Send an email notification."""
        if not self.enabled or not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.warning("Email notifications not configured")
            return False
        
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            
            if html:
                message.attach(MIMEText(body, "html"))
            else:
                message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            logger.info(f"Email sent: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def notify_high_match_job(self, job: Dict[str, Any]):
        """Notify user of a high-match job."""
        match_score = job.get("match_score", 0)
        
        subject = f"🎯 High Match Job Alert: {job['title']} ({match_score:.0f}% match)"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #2557a7 0%, #1a4180 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0;">🎯 High Match Job Found!</h1>
            </div>
            
            <div style="padding: 20px; background: #f9fafb; border: 1px solid #e5e7eb;">
                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 16px;">
                    <h2 style="color: #1f2937; margin-top: 0;">{job['title']}</h2>
                    <p style="color: #6b7280; font-size: 16px; margin: 8px 0;">
                        <strong>{job['company']}</strong> • {job['location']}
                    </p>
                    
                    <div style="background: #d1fae5; color: #10b981; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 600; margin: 16px 0;">
                        {match_score:.0f}% Match Score
                    </div>
                    
                    <p style="color: #374151; line-height: 1.6; margin: 16px 0;">
                        {job.get('raw_description', 'No description')[:200]}...
                    </p>
                    
                    <a href="{job['url']}" style="display: inline-block; background: #2557a7; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 16px;">
                        View Job Details
                    </a>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <h3 style="color: #1f2937; margin-top: 0;">Why this is a great match:</h3>
                    <ul style="color: #374151; line-height: 1.8;">
                        <li>Skills alignment: {len(job.get('parsed_data', {}).get('skills', []))} matching skills</li>
                        <li>Experience level: {job.get('parsed_data', {}).get('seniority', 'Not specified')}</li>
                        <li>Location: {job['location']}</li>
                    </ul>
                </div>
            </div>
            
            <div style="padding: 16px; text-align: center; color: #6b7280; font-size: 14px;">
                <p>Powered by Career Agent AI</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subject, html_body, html=True)
    
    def notify_application_submitted(self, job: Dict[str, Any], cover_letter: str):
        """Notify user of successful application submission."""
        subject = f"✅ Application Submitted: {job['title']}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0;">✅ Application Submitted Successfully!</h1>
            </div>
            
            <div style="padding: 20px; background: #f9fafb;">
                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #1f2937; margin-top: 0;">{job['title']}</h2>
                    <p style="color: #6b7280;"><strong>{job['company']}</strong> • {job['location']}</p>
                    
                    <p style="color: #374151; margin: 16px 0;">
                        Your application has been automatically submitted with a tailored resume and cover letter.
                    </p>
                    
                    <a href="{job['url']}" style="display: inline-block; background: #2557a7; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 8px;">
                        Track Application
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subject, html_body, html=True)
    
    def send_daily_summary(self, stats: Dict[str, Any]):
        """Send daily summary of job search activity."""
        subject = f"📊 Daily Job Search Summary - {stats.get('jobs_scraped', 0)} new jobs"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0;">📊 Daily Summary</h1>
            </div>
            
            <div style="padding: 20px; background: #f9fafb;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                    <div style="background: white; padding: 16px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 32px; font-weight: 700; color: #2557a7;">{stats.get('jobs_scraped', 0)}</div>
                        <div style="color: #6b7280; margin-top: 4px;">Jobs Scraped</div>
                    </div>
                    <div style="background: white; padding: 16px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 32px; font-weight: 700; color: #10b981;">{stats.get('high_match', 0)}</div>
                        <div style="color: #6b7280; margin-top: 4px;">High Matches</div>
                    </div>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <h3 style="color: #1f2937; margin-top: 0;">Top Skills in Demand</h3>
                    <ul style="color: #374151;">
                        {''.join(f"<li>{skill['skill']}: {skill['count']} jobs</li>" for skill in stats.get('top_skills', [])[:5])}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subject, html_body, html=True)


# Global notification service instance
notification_service = NotificationService()
