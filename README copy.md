# PR Review Bot

A GitHub Actions-based bot that uses Blackbox API to automatically review Pull Requests with AI-powered analysis, bug detection, documentation linking, and summarization.

## Features

- **Out-of-the-box**: Works immediately after setup in any GitHub repository.
- **Robust & Scalable**: Handles multiple repositories without per-repo configuration.
- **Innovative Analysis**:
  - Code review with suggestions.
  - Bug detection.
  - Documentation linking.
  - Change summarization.
- **Clear Demo**: See below for testing instructions.

## Setup

1. **Fork or Clone this repository** to your GitHub account.

2. **Add Repository Secrets** (in Settings > Secrets and variables > Actions):
   - `BLACKBOX_API_KEY`: Your Blackbox API key.
   - `BLACKBOX_API_URL`: (Optional) Blackbox API endpoint URL. Defaults to `https://api.blackbox.ai/v1/completions`.

3. **Copy the workflow** to your target repository:
   - Copy `.github/workflows/pr-review.yml` to the target repo's `.github/workflows/` directory.
   - Copy `review_pr.py` to the root of the target repo.

4. **Install Dependencies** (if running locally):
   - `pip install requests PyGithub`

## How It Works

- Triggers on PR events: opened, synchronize, reopened.
- Fetches the PR diff using GitHub API.
- Sends the diff to Blackbox API with a structured prompt for analysis.
- Posts an AI-generated comment on the PR with review insights.

## Demo

### Local Testing

1. Install dependencies:
   ```bash
   pip install requests PyGithub
   ```

2. Run the test script:
   ```bash
   python test_locally.py
   ```
   This will simulate PR analysis with mock data and test error handling.

### GitHub Testing

1. Push this repository to GitHub or copy the files to an existing repo.
2. Add the required secrets in repository settings.
3. Create a PR in the repository.
4. The bot will automatically trigger and post a review comment.

### Sample Output

The bot generates comments like:

```
## PR Review by Blackbox AI

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
```

## Customization

- Modify the prompt in `review_pr.py` to adjust analysis focus.
- Add more API integrations or post-processing logic.

## Requirements

- Python 3.9+
- GitHub Actions enabled in the repository.
- Valid Blackbox API credentials.

## License

MIT
