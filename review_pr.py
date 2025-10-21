import os
import requests
import json
from github import Github

def get_pr_diff(repo_name, pr_number, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    diff = pr.get_files()
    diff_text = ""
    for file in diff:
        diff_text += f"File: {file.filename}\n"
        if file.patch:
            diff_text += file.patch + "\n\n"
    return diff_text, pr.title, pr.body

def analyze_with_blackbox(diff, title, body, api_key, api_url):
    prompt = f"""
Analyze the following Pull Request for code review:

Title: {title}
Description: {body or "No description"}

Diff:
{diff}

Please provide:
1. A summary of the changes.
2. Potential bugs or issues in the code.
3. Suggestions for improvements.
4. Links to relevant documentation if applicable.
5. Overall assessment.

Keep the response concise and actionable.
"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 1000
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('response', 'No response from Blackbox API')
    else:
        raise Exception(f"Blackbox API error: {response.status_code} - {response.text}")

def post_comment(repo_name, pr_number, comment, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)

def main():
    repo_name = os.getenv('GITHUB_REPOSITORY')
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if event_path:
        with open(event_path, 'r') as f:
            event = json.load(f)
        pr_number = event['number']
    else:
        pr_number = int(os.getenv('PR_NUMBER', 1))  # For local testing
    token = os.getenv('GITHUB_TOKEN')
    api_key = os.getenv('BLACKBOX_API_KEY')
    api_url = os.getenv('BLACKBOX_API_URL', 'https://api.blackbox.ai/v1/completions')  # Default URL, adjust as needed

    try:
        diff, title, body = get_pr_diff(repo_name, pr_number, token)
        if len(diff) > 50000:  # Limit diff size
            diff = diff[:50000] + "\n\n[Diff truncated due to size]"
        analysis = analyze_with_blackbox(diff, title, body, api_key, api_url)
        comment = f"## PR Review by Blackbox AI\n\n{analysis}"
        post_comment(repo_name, pr_number, comment, token)
        print("PR review comment posted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        # Optionally post an error comment
        try:
            error_comment = f"## PR Review Error\n\nFailed to analyze PR: {str(e)}"
            post_comment(repo_name, pr_number, error_comment, token)
        except:
            print("Failed to post error comment.")

if __name__ == "__main__":
    main()
