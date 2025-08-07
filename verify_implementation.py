"""
Simple verification of the EmailProcessor implementation
"""
import os
import sys

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import the modules
from email_processor import EmailProcessor
from gmail_client import Email, MockGmailClient

# Test 1: Basic filter functionality
print("Test 1: Filter emails with all keywords")
mock_client = MockGmailClient()
processor = EmailProcessor(mock_client)

emails = [
    Email("1", "pseudo internship interest", "body", "sender@test.com", "recipient@test.com"),
    Email("2", "job application", "body", "sender@test.com", "recipient@test.com"),
    Email("3", "PSEUDO INTERNSHIP INTEREST APPLICATION", "body", "sender@test.com", "recipient@test.com"),
]

filtered = processor.filter_emails(emails)
print(f"Filtered count: {len(filtered)} (expected: 2)")
print(f"Filtered IDs: {[email.id for email in filtered]}")
print(f"Test 1 PASSED: {len(filtered) == 2 and filtered[0].id == '1' and filtered[1].id == '3'}")
print()

# Test 2: Name extraction
print("Test 2: Name extraction from email bodies")
test_cases = [
    ("Email body\nBest regards,\nJohn Smith", "John Smith"),
    ("Email body\nSincerely,\nEmily Johnson", "Emily Johnson"),
    ("Email body\nThanks,\nMichael Brown", "Michael Brown"),
    ("Email body\nRegards,\nSarah Davis", "Sarah Davis"),
    ("Email body\nBest,\nDavid Wilson", "David Wilson"),
    ("Email body with no signature", None),
]

all_name_tests_passed = True
for email_body, expected_name in test_cases:
    result = processor.extract_name_from_email(email_body)
    passed = result == expected_name
    print(f"Expected: {expected_name}, Got: {result}, Passed: {passed}")
    if not passed:
        all_name_tests_passed = False

print(f"Test 2 PASSED: {all_name_tests_passed}")
print()

# Test 3: Response generation
print("Test 3: Response generation")
response_with_name = processor.generate_response("John Smith")
response_without_name = processor.generate_response(None)

name_test = "Dear John Smith," in response_with_name and "Thank you for your interest" in response_with_name
no_name_test = "Dear Applicant," in response_without_name and "Thank you for your interest" in response_without_name

print(f"Response with name test PASSED: {name_test}")
print(f"Response without name test PASSED: {no_name_test}")
print()

# Test 4: End-to-end processing
print("Test 4: End-to-end email processing")
test_emails = [
    Email("1", "pseudo internship interest", "Hi there!\nBest regards,\nAlice Smith", "alice@test.com", "hiring@company.com"),
    Email("2", "pseudo internship interest", "Hello!\nThanks,\nBob Johnson", "bob@test.com", "hiring@company.com"),
    Email("3", "job application", "Hi!", "charlie@test.com", "hiring@company.com"),  # Should be filtered out
]

mock_client = MockGmailClient(test_emails)
processor = EmailProcessor(mock_client)

result = processor.process_emails()

print(f"Total emails: {result['total_emails']} (expected: 3)")
print(f"Filtered emails: {result['filtered_emails']} (expected: 2)")
print(f"Responses sent: {result['responses_sent']} (expected: 2)")
print(f"Sent emails count: {len(mock_client.sent_emails)}")

end_to_end_test = (
    result['total_emails'] == 3 and
    result['filtered_emails'] == 2 and
    result['responses_sent'] == 2 and
    len(mock_client.sent_emails) == 2
)

print(f"Test 4 PASSED: {end_to_end_test}")

# Print sent email details
print("\nSent emails:")
for i, sent_email in enumerate(mock_client.sent_emails):
    print(f"Email {i+1}:")
    print(f"  To: {sent_email['to']}")
    print(f"  Subject: {sent_email['subject']}")
    print(f"  Body preview: {sent_email['body'][:100]}...")
    print()

print(f"\nOVERALL RESULT: All tests passed: {len(filtered) == 2 and all_name_tests_passed and name_test and no_name_test and end_to_end_test}")
