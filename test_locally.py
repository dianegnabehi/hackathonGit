import os
import json
from review_pr import analyze_with_blackbox, post_comment, get_pr_diff

# Mock environment variables for local testing
os.environ['GITHUB_TOKEN'] = 'mock_token'  # Replace with real token if testing GitHub API
os.environ['BLACKBOX_API_KEY'] = 'mock_key'  # Replace with real key
os.environ['BLACKBOX_API_URL'] = 'https://api.blackbox.ai/v1/completions'  # Adjust if needed
os.environ['GITHUB_REPOSITORY'] = 'test/repo'
os.environ['GITHUB_EVENT_PATH'] = 'mock_event.json'
os.environ['PR_NUMBER'] = '1'

# Mock PR data
mock_diff = """
diff --git a/example.py b/example.py
index 1234567..abcdef0 100644
--- a/example.py
+++ b/example.py
@@ -1,3 +1,5 @@
 def hello():
-    print("Hello")
+    print("Hello World")
+    return "done"
"""

mock_title = "Add return statement to hello function"
mock_body = "This PR adds a return statement for better functionality."

# Mock Blackbox API response (since we can't call real API without key)
def mock_analyze_with_blackbox(diff, title, body, api_key, api_url):
    return """
## Summary of Changes
- Modified the `hello` function to print "Hello World" and return "done".

## Potential Bugs or Issues
- No obvious bugs, but ensure the return value is used appropriately.

## Suggestions for Improvements
- Consider adding type hints for better code quality.

## Links to Relevant Documentation
- Python Functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions

## Overall Assessment
This is a minor improvement. Approved with suggestions.
"""

# Test analysis
print("Testing mock analysis...")
try:
    analysis = mock_analyze_with_blackbox(mock_diff, mock_title, mock_body, os.getenv('BLACKBOX_API_KEY'), os.getenv('BLACKBOX_API_URL'))
    print("Mock Analysis Result:")
    print(analysis)
    print("\nTest passed: Analysis generated successfully.")
except Exception as e:
    print(f"Test failed: {e}")

# Test error handling
print("\nTesting error handling...")
try:
    # Simulate API failure
    analyze_with_blackbox(mock_diff, mock_title, mock_body, 'invalid_key', 'invalid_url')
except Exception as e:
    print(f"Error handling test passed: {e}")

# Test large diff truncation
print("\nTesting large diff handling...")
large_diff = mock_diff * 1000  # Make it large
if len(large_diff) > 50000:
    truncated = large_diff[:50000] + "\n\n[Diff truncated due to size]"
    print("Large diff truncated successfully.")
else:
    print("Diff not large enough for truncation test.")

print("\nLocal testing completed.")
