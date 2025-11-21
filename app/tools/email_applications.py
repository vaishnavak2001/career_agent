"""Automated job application system with email-based submissions."""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class EmailApplicationSender:
    """
    Sends job applications via email with resume and cover letter attachments
    
    Setup:
    1. For Gmail, enable 2FA and create an app password:
       https://support.google.com/accounts/answer/185833
    2. Set environment variables:
       - SMTP_HOST (default: smtp.gmail.com)
       - SMTP_PORT (default: 587)
       - SMTP_USER (your email)
       - SMTP_PASSWORD (app password)
    """
    
    def __init__(
        self,
        smtp_host: str = None,
        smtp_port: int = None,
        smtp_user: str = None,
        smtp_password: str = None
    ):
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        
        # Check for dry run mode
        self.dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
        
        if not self.smtp_user or not self.smtp_password:
            logger.warning("Email credentials not configured. Set SMTP_USER and SMTP_PASSWORD in .env")
    
    def send_application(
        self,
        to_email: str,
        job_title: str,
        company_name: str,
        resume_path: Optional[str] = None,
        resume_content: Optional[str] = None,
        cover_letter_content: Optional[str] = None,
        applicant_name: str = "Job Seeker",
        applicant_email: str = None
    ) -> Dict[str, Any]:
        """
        Send a job application via email
        
        Args:
            to_email: Recipient email (HR/recruiter)
            job_title: Position title
            company_name: Company name
            resume_path: Path to PDF resume file
            resume_content: Resume text content (if PDF not provided)
            cover_letter_content: Cover letter text
            applicant_name: Your name
            applicant_email: Your email (defaults to SMTP_USER)
        
        Returns:
            Dict with status and message
        """
        if not applicant_email:
            applicant_email = self.smtp_user
        
        # Validate email format
        if not self._is_valid_email(to_email):
            return {
                "success": False,
                "message": f"Invalid recipient email: {to_email}"
            }
        
        # Check dry run mode
        if self.dry_run:
            logger.info(f"[DRY RUN] Would send application to {to_email} for {job_title} at {company_name}")
            return {
                "success": True,
                "message": "Application simulated (DRY RUN mode)",
                "dry_run": True
            }
        
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"{applicant_name} <{applicant_email}>"
            msg['To'] = to_email
            msg['Subject'] = f"Application for {job_title} Position"
            
            # Email body
            body = self._create_email_body(
                job_title=job_title,
                company_name=company_name,
                applicant_name=applicant_name,
                cover_letter_content=cover_letter_content
            )
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach resume PDF if provided
            if resume_path and Path(resume_path).exists():
                self._attach_file(msg, resume_path, "resume.pdf")
            elif resume_content:
                # Create resume text attachment
                attachment = MIMEText(resume_content, 'plain')
                attachment.add_header('Content-Disposition', 'attachment', filename='resume.txt')
                msg.attach(attachment)
            
            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Application sent to {to_email} for {job_title} at {company_name}")
            
            return {
                "success": True,
                "message": f"Application sent successfully to {to_email}",
                "sent_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send application: {e}")
            return {
                "success": False,
                "message": f"Email send failed: {str(e)}"
            }
    
    def _create_email_body(
        self,
        job_title: str,
        company_name: str,
        applicant_name: str,
        cover_letter_content: Optional[str] = None
    ) -> str:
        """Create professional email body"""
        
        if cover_letter_content:
            # Use provided cover letter
            return cover_letter_content
        
        # Default template
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}.

I have attached my resume for your review. I believe my skills and experience make me a great fit for this role, and I would welcome the opportunity to discuss how I can contribute to your team.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
{applicant_name}

---
This is an automated application sent via Career Agent.
Please review the attached resume for detailed information about my qualifications.
"""
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str, filename: str = None):
        """Attach a file to email message"""
        if not filename:
            filename = Path(file_path).name
        
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


def extract_email_from_job_description(job_description: str) -> Optional[str]:
    """
    Extract email address from job description
    
    Args:
        job_description: Job description text
    
    Returns:
        First email found, or None
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, job_description)
    
    # Filter out common non-recruiter emails
    for email in matches:
        email_lower = email.lower()
        if not any(skip in email_lower for skip in ['noreply', 'no-reply', 'donotreply']):
            return email
    
    return None


def should_auto_apply(job_data: Dict[str, Any], min_match_score: float = 75.0) -> bool:
    """
    Determine if a job should receive auto-application
    
    Criteria:
    - Match score >= threshold
    - Not flagged as scam
    - Has valid application email
    - Not already applied
    
    Args:
        job_data: Job dictionary with match_score, is_scam, etc.
        min_match_score: Minimum match score required
    
    Returns:
        True if should auto-apply, False otherwise
    """
    match_score = job_data.get("match_score", 0)
    is_scam = job_data.get("is_scam", False)
    status = job_data.get("status", "")
    
    # Check match score
    if match_score < min_match_score:
        logger.debug(f"Skip: Match score {match_score} < {min_match_score}")
        return False
    
    # Check scam flag
    if is_scam:
        logger.debug("Skip: Flagged as potential scam")
        return False
    
    # Check if already applied
    if status in ["applied", "submitted"]:
        logger.debug("Skip: Already applied")
        return False
    
    # Check for application email
    email = extract_email_from_job_description(job_data.get("raw_description", ""))
    if not email:
        logger.debug("Skip: No application email found")
        return False
    
    logger.info(f"✅ Auto-apply candidate: {job_data.get('title')} at {job_data.get('company')}")
    return True


# Convenience function
def send_job_application(
    job_data: Dict[str, Any],
    resume_path: str = None,
    cover_letter: str = None,
    applicant_name: str = "Job Seeker"
) -> Dict[str, Any]:
    """
    Quick function to send a job application
    
    Usage:
        result = send_job_application(
            job_data=my_job,
            resume_path="/path/to/resume.pdf",
            cover_letter=generated_cover_letter
        )
    """
    # Extract email from job description
    to_email = extract_email_from_job_description(job_data.get("raw_description", ""))
    
    if not to_email:
        return {
            "success": False,
            "message": "No application email found in job description"
        }
    
    sender = EmailApplicationSender()
    
    return sender.send_application(
        to_email=to_email,
        job_title=job_data.get("title", "Unknown Position"),
        company_name=job_data.get("company", "Unknown Company"),
        resume_path=resume_path,
        cover_letter_content=cover_letter,
        applicant_name=applicant_name
    )
