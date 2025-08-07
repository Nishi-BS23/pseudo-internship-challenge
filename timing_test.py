"""Test with time logging to understand bottlenecks"""
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from src.email_processor import EmailProcessor
from src.gmail_client import MockGmailClient
from tests.test_data_generator import TestDataGenerator

data_generator = TestDataGenerator()

# Create a smaller test to verify our logic
print("Testing with 25 emails (should take ~3.5s):")
test_emails = data_generator.generate_test_emails(25)
mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

start_time = time.time()

# Time each step
fetch_start = time.time()
emails = mock_client.fetch_emails()
fetch_time = time.time() - fetch_start

filter_start = time.time()
filtered_emails = processor.filter_emails(emails)
filter_time = time.time() - filter_start

print(f"Fetch time: {fetch_time:.3f}s")
print(f"Filter time: {filter_time:.3f}s")
print(f"Emails to process: {len(filtered_emails)}")

send_start = time.time()
responses_sent = 0
for email in filtered_emails:
    name = processor.extract_name_from_email(email.body)
    response_body = processor.generate_response(name)
    reply_subject = f"Re: {email.subject}"
    
    if mock_client.send_email(email.sender, reply_subject, response_body):
        responses_sent += 1

send_time = time.time() - send_start
total_time = time.time() - start_time

print(f"Send time: {send_time:.3f}s")
print(f"Total time: {total_time:.3f}s")
print(f"Responses sent: {responses_sent}")
print(f"Expected send time: {len(filtered_emails) * 0.2:.1f}s")
print(f"Expected total time: {0.2 + len(filtered_emails) * 0.2:.1f}s")
