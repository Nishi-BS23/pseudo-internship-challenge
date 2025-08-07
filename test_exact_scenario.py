"""Test the exact scenario from failing tests"""
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from src.email_processor import EmailProcessor
from src.gmail_client import MockGmailClient
from tests.test_data_generator import TestDataGenerator

data_generator = TestDataGenerator()

print("Testing with 500 emails (exact test scenario):")
test_emails = data_generator.generate_test_emails(500)
mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

# Let's check the filtering first without sending
filtered_emails = processor.filter_emails(test_emails)
print(f"Total: {len(test_emails)}, Filtered: {len(filtered_emails)}")
print(f"Estimated send time: {len(filtered_emails) * 0.2:.1f}s")
print(f"Total estimated time: {0.2 + len(filtered_emails) * 0.2:.1f}s")

# Now test just filtering performance
start_time = time.time()
filtered = processor.filter_emails(test_emails)
filter_time = time.time() - start_time
print(f"Filter time: {filter_time:.3f}s")

# Test name extraction on a sample
start_time = time.time()
for email in filtered[:10]:
    processor.extract_name_from_email(email.body)
extract_time = time.time() - start_time
print(f"Name extraction time for 10 emails: {extract_time:.3f}s")
print(f"Estimated total name extraction time: {extract_time * len(filtered) / 10:.3f}s")
