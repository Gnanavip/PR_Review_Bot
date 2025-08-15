# PR_Review_Bot

## Overview
PR_Review_Bot automatically reviews pull requests in a GitHub repository using AI, providing feedback on code quality, best practices, and potential improvements. The bot runs via GitHub Actions, requiring no manual intervention once configured.

---

## Features
- Automatically triggered on pull requests.
- Uses GitHub Actions for CI/CD automation.
- Reads secrets securely from GitHub repository settings.
- Easily reusable in multiple repositories.

---

## Requirements
- Python 3.11+
- GitHub repository secrets:
  - `OPENROUTER_API_KEY`
  - `GITHUB_TOKEN`
- Installed Python packages listed in `requirements.txt`

---

## Setup & Local Run

1. **Clone the repository**
```bash
git clone https://github.com/<your-username>/PR_Review_Bot.git
cd PR_Review_Bot
```

2. **Create a virtual environment**
```bash
python -m venv venv
# Activate the environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```
**3. Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Set environment variables locally**
```bash
# Linux/Mac
export OPENROUTER_API_KEY="<your_api_key>"
export GITHUB_TOKEN="<your_github_token>"

# Windows (PowerShell)
setx OPENROUTER_API_KEY "<your_api_key>"
setx GITHUB_TOKEN "<your_github_token>"
```

5. **Run the bot**
```bash
python pr_review_bot.py --owner <your-username> --repo PR_Review_Bot --pr <PR_number>
```



