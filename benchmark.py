"""Benchmark to understand performance bottlenecks"""
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from src.email_processor import EmailProcessor
from src.gmail_client import MockGmailClient
from tests.test_data_generator import TestDataGenerator

# Test with small dataset to understand timing
data_generator = TestDataGenerator()

print("Testing with 10 emails:")
test_emails = data_generator.generate_test_emails(10)
mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

start_time = time.time()
result = processor.process_emails()
end_time = time.time()

print(f"Time: {end_time - start_time:.2f}s")
print(f"Total: {result['total_emails']}, Filtered: {result['filtered_emails']}, Sent: {result['responses_sent']}")
print(f"Expected time: {0.2 + (result['filtered_emails'] * 0.2):.2f}s")
print()

print("Testing with 50 emails:")
test_emails = data_generator.generate_test_emails(50)
mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

start_time = time.time()
result = processor.process_emails()
end_time = time.time()

print(f"Time: {end_time - start_time:.2f}s")
print(f"Total: {result['total_emails']}, Filtered: {result['filtered_emails']}, Sent: {result['responses_sent']}")
print(f"Expected time: {0.2 + (result['filtered_emails'] * 0.2):.2f}s")
