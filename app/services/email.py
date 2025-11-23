import logging
from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.sender = settings.EMAIL_FROM

    async def send_email(self, to_email: str, subject: str, content: str):
        """
        Send an email using SendGrid.
        """
        if not self.api_key:
            logger.warning("SendGrid API key not set. Email sending skipped.")
            return False

        message = Mail(
            from_email=self.sender,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )

        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            logger.info(f"Email sent to {to_email}. Status code: {response.status_code}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    async def send_job_alert(self, to_email: str, jobs: List[dict]):
        """
        Send a job alert email with a list of matched jobs.
        """
        if not jobs:
            return
            
        subject = f"Found {len(jobs)} New Jobs Matching Your Profile"
        
        # Build HTML content
        job_list_html = ""
        for job in jobs:
            job_list_html += f"""
            <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                <h3 style="margin: 0 0 10px 0;"><a href="{job.get('url')}">{job.get('title')}</a></h3>
                <p style="margin: 5px 0;"><strong>Company:</strong> {job.get('company')}</p>
                <p style="margin: 5px 0;"><strong>Location:</strong> {job.get('location')}</p>
                <p style="margin: 5px 0;"><strong>Match Score:</strong> {job.get('match_score')}%</p>
            </div>
            """
            
        content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2>New Job Matches Found!</h2>
                <p>Hello,</p>
                <p>We found {len(jobs)} new jobs that match your preferences:</p>
                {job_list_html}
                <p>Good luck with your applications!</p>
                <p><em>Autonomous Career Agent</em></p>
            </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, content)

email_service = EmailService()
