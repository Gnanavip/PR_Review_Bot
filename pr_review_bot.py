import os
import sys
from github import Github
from dotenv import load_dotenv
import openrouter

# Load local .env if present (for local development)
load_dotenv()

def load_tokens():
    gh_token = os.getenv("GITHUB_TOKEN")
    or_key = os.getenv("OPENROUTER_API_KEY")
    if not gh_token:
        raise RuntimeError("GITHUB_TOKEN missing. Set it in environment variables or .env file.")
    if not or_key:
        raise RuntimeError("OPENROUTER_API_KEY missing. Set it in environment variables or .env file.")
    return gh_token, or_key

def get_ai_suggestion(file_content, file_name, or_key):
    client = openrouter.OpenRouter(api_key=or_key)
    prompt = f"Analyze this code file named {file_name} and provide suggestions for coding style, best practices, and improvements:\n\n{file_content}"
    response = client.completions.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

def main():
    if len(sys.argv) != 3:
        print("Usage: python pr_review_bot.py <repo_name> <pr_number>")
        sys.exit(1)

    repo_name = sys.argv[1]
    pr_number = int(sys.argv[2])

    gh_token, or_key = load_tokens()
    print("Tokens loaded successfully. Bot is running...\n")

    # Connect to GitHub
    g = Github(gh_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # List changed files
    changed_files = [f.filename for f in pr.get_files()]
    print(f"Changed files in PR #{pr_number}:")
    for f in changed_files:
        print(f"- {f}")

    # Generate AI suggestions and post comments
    for file in changed_files:
        try:
            content = repo.get_contents(file, ref=pr.head.ref).decoded_content.decode()
        except Exception as e:
            print(f"Could not fetch content for {file}: {e}")
            content = ""
        suggestion = get_ai_suggestion(content, file, or_key)
        pr.create_issue_comment(f"**AI Suggestion for {file}:**\n{suggestion}")
        print(f"Posted suggestion for {file}")

    print(f"\nAll AI suggestions posted to PR #{pr_number} successfully!")

if __name__ == "__main__":
    main()
