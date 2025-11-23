"""
Scam Detection Service
Analyzes jobs for potential scam indicators
"""

class ScamDetector:
    def __init__(self):
        self.suspicious_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'protonmail.com']
        self.spam_keywords = ['payment upfront', 'wire transfer', 'western union', 'pay fee', 
                             'processing fee', 'training fee', 'background check fee']
    
    def detect_scam(self, job_record: dict) -> dict:
        """
        Detect if a job listing is potentially a scam.
        Returns: {is_scam: bool, score: int, flags: list}
        """
        flags = []
        score = 0
        
        # Check company email domain
        company = job_record.get('company', '').lower()
        raw_text = job_record.get('raw_text', '').lower()
        
        # Flag 1: Suspicious email domain in company contact
        for domain in self.suspicious_domains:
            if domain in raw_text and 'contact' in raw_text:
                flags.append(f"Uses free email domain ({domain}) for contact")
                score += 30
                break
        
        # Flag 2: Payment requests
        for keyword in self.spam_keywords:
            if keyword in raw_text:
                flags.append(f"Contains suspicious keyword: '{keyword}'")
                score += 40
        
        # Flag 3: Unrealistic salary
        if 'salary' in raw_text:
            if any(word in raw_text for word in ['million', '500k', '1000k']):
                flags.append("Unrealistic compensation mentioned")
                score += 20
        
        # Flag 4: Missing company details
        if len(company) < 3:
            flags.append("Company name missing or too short")
            score += 15
        
        # Flag 5: Too good to be true indicators
        if any(phrase in raw_text for phrase in ['work from home', 'no experience', 'guaranteed income']):
            if any(phrase in raw_text for phrase in ['easy money', 'quick cash', 'earn thousands']):
                flags.append("Too good to be true indicators")
                score += 25
        
        is_scam = score >= 50
        
        return {
            "is_scam": is_scam,
            "score": min(score, 100),
            "flags": flags
        }

scam_detector_service = ScamDetector()
