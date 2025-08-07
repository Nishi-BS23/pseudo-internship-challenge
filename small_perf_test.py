"""Quick performance test"""
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from src.email_processor import EmailProcessor
from src.gmail_client import MockGmailClient
from tests.test_data_generator import TestDataGenerator

data_generator = TestDataGenerator()

# Test with 20 emails to see timing
test_emails = data_generator.generate_test_emails(20)
mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

start_time = time.time()
result = processor.process_emails()
end_time = time.time()

actual_time = end_time - start_time
expected_time = 0.2 + (result['filtered_emails'] * 0.2)

print(f"20 emails test:")
print(f"Filtered: {result['filtered_emails']}")
print(f"Actual time: {actual_time:.3f}s")
print(f"Expected time: {expected_time:.3f}s")
print(f"Overhead: {actual_time - expected_time:.3f}s")
