"""Quick test to check filtering efficiency"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from src.email_processor import EmailProcessor
from src.gmail_client import MockGmailClient
from tests.test_data_generator import TestDataGenerator

# Test with a smaller dataset first
data_generator = TestDataGenerator()
test_emails = data_generator.generate_test_emails(100)

mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

# Check filtering
filtered_emails = processor.filter_emails(test_emails)

print(f"Total emails: {len(test_emails)}")
print(f"Filtered emails: {len(filtered_emails)}")
print(f"Filter percentage: {len(filtered_emails) / len(test_emails) * 100:.1f}%")

# Check a few examples
print("\nFirst 5 email subjects and filter results:")
for i, email in enumerate(test_emails[:5]):
    is_filtered = email in filtered_emails
    print(f"{i+1}. '{email.subject}' -> {'PASS' if is_filtered else 'FAIL'}")
