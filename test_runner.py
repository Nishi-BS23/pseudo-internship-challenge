#!/usr/bin/env python
"""Simple test runner to verify our implementation"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.email_processor import EmailProcessor
from src.gmail_client import Email, MockGmailClient

def test_filter_functionality():
    """Test the filter_emails functionality"""
    mock_client = MockGmailClient()
    processor = EmailProcessor(mock_client)

    emails = [
        Email(
            "1",
            "pseudo internship interest",
            "body",
            "sender@test.com",
            "recipient@test.com",
        ),
        Email(
            "2", "job application", "body", "sender@test.com", "recipient@test.com"
        ),
        Email(
            "3",
            "PSEUDO INTERNSHIP INTEREST APPLICATION",
            "body",
            "sender@test.com",
            "recipient@test.com",
        ),
    ]

    filtered = processor.filter_emails(emails)
    print(f"Filtered emails count: {len(filtered)}")
    print(f"Expected: 2")
    print(f"Test passed: {len(filtered) == 2}")
    return len(filtered) == 2

def test_name_extraction():
    """Test the extract_name_from_email functionality"""
    mock_client = MockGmailClient()
    processor = EmailProcessor(mock_client)

    test_cases = [
        ("Email body\nBest regards,\nJohn Smith", "John Smith"),
        ("Email body\nSincerely,\nEmily Johnson", "Emily Johnson"),
        ("Email body\nThanks,\nMichael Brown", "Michael Brown"),
        ("Email body\nRegards,\nSarah Davis", "Sarah Davis"),
        ("Email body\nBest,\nDavid Wilson", "David Wilson"),
        ("Email body with no signature", None),
    ]

    all_passed = True
    for email_body, expected_name in test_cases:
        result = processor.extract_name_from_email(email_body)
        passed = result == expected_name
        print(f"Input: {email_body[:30]}... Expected: {expected_name}, Got: {result}, Passed: {passed}")
        if not passed:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("Testing filter functionality...")
    filter_test = test_filter_functionality()
    print()
    
    print("Testing name extraction functionality...")
    name_test = test_name_extraction()
    print()
    
    print(f"Filter test passed: {filter_test}")
    print(f"Name extraction test passed: {name_test}")
    print(f"All tests passed: {filter_test and name_test}")
