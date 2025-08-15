import os
from github import Github

def load_tokens():
    gh = os.getenv("GITHUB_TOKEN")
    or_key = os.getenv("OPENROUTER_API_KEY")
    if not gh:
        raise RuntimeError("GITHUB_TOKEN missing. Make sure it is set in GitHub Actions secrets!")
    if not or_key:
        raise RuntimeError("OPENROUTER_API_KEY missing. Make sure it is set in GitHub Actions secrets!")
    return gh, or_key

def main():
    gh_token, or_key = load_tokens()
    print("Tokens loaded successfully. Bot is running...\n")

    # Connect to GitHub
    g = Github(gh_token)
    repo_name = "Gnanavip/PR_Review_Bot"  # Change to your demo repo
    repo = g.get_repo(repo_name)
    
    # PR number to analyze (you can read this from a .dat file if needed)
    pr_number = 1
    pr = repo.get_pull(pr_number)
    
    # List changed files
    changed_files = [f.filename for f in pr.get_files()]
    print(f"Changed files in PR #{pr_number}:")
    for f in changed_files:
        print(f"- {f}")

    # Example AI suggestion (replace with real AI analysis if available)
    suggestions = []
    for file in changed_files:
        suggestions.append(f"Suggestion for {file}: Check coding style and best practices.")

    # Post suggestions as PR comments
    for suggestion in suggestions:
        pr.create_issue_comment(suggestion)
        print(f"Posted comment: {suggestion}")

    print(f"\nAll suggestions posted to PR #{pr_number} successfully!")

if __name__ == "__main__":
    main()
