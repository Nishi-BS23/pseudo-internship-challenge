import time
import re

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        
        # Compile regex patterns once for better performance
        self.name_patterns = [
            re.compile(r"Best regards,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Sincerely,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Thanks,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Regards,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Best,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Thank you,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Kind regards,\s*([A-Za-z\s]+)", re.IGNORECASE),
        ]
        self.name_validator = re.compile(r"^[A-Za-z\s]+$")

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            # Check if all required keywords are present in the subject
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        # implement name extraction logic using pre-compiled patterns
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                name = match.group(1).strip()
                # Return only if name contains letters and is not empty
                if name and self.name_validator.match(name):
                    return name
        
        return None

    # Use this method. Do not modify it.
    def generate_response(self, name: str | None) -> str:
        if name:
            return f"""Dear {name},

Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""
        else:
            return """Dear Applicant,

Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # Optimized email processing logic
        # Fetch all emails from the client (single call)
        emails = self.gmail_client.fetch_emails()
        
        # Filter emails based on required keywords (optimized)
        filtered_emails = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered_emails.append(email)
        
        # Process each filtered email and send responses (minimized operations)
        for email in filtered_emails:
            # Extract name from email body using pre-compiled regex
            name = None
            for pattern in self.name_patterns:
                match = pattern.search(email.body)
                if match:
                    extracted = match.group(1).strip()
                    if extracted and self.name_validator.match(extracted):
                        name = extracted
                        break
            
            # Generate response and send (minimal operations)
            response_body = self.generate_response(name)
            
            # Send response email
            if self.gmail_client.send_email(email.sender, f"Re: {email.subject}", response_body):
                responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
