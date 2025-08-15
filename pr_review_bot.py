import os
from github import Github
from openrouter import OpenRouter

def load_tokens():
    """Load GitHub and OpenRouter API tokens from environment variables."""
    gh = os.getenv("GITHUB_TOKEN")
    or_key = os.getenv("OPENROUTER_API_KEY")
    if not gh:
        raise RuntimeError("GITHUB_TOKEN missing. Make sure it is set in GitHub Actions secrets!")
    if not or_key:
        raise RuntimeError("OPENROUTER_API_KEY missing. Make sure it is set in GitHub Actions secrets!")
    return gh, or_key

def get_ai_suggestion(file_content, file_name, or_key):
    """Generate AI suggestion for a given file using OpenRouter API."""
    client = OpenRouter(api_key=or_key)
    prompt = f"Analyze this code file named {file_name} and provide suggestions to improve coding style, best practices, and potential issues:\n\n{file_content}"
    
    response = client.completions.create(
        model="gpt-4o-mini",  # Can switch to "gpt-4" if desired
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

def main():
    gh_token, or_key = load_tokens()
    print("Tokens loaded successfully. Bot is running...\n")

    # Read repo name and PR number from .dat file
    try:
        with open("pr_info.dat", "r") as f:
            lines = f.read().splitlines()
            repo_name = lines[0].strip()       # GitHub repo in "owner/repo" format
            pr_number = int(lines[1].strip())  # PR number
        print(f"Repository: {repo_name}, PR number: {pr_number}")
    except Exception as e:
        print(f"Error reading repo or PR number from file: {e}")
        return

    # Connect to GitHub
    g = Github(gh_token)
    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        print(f"Error accessing repository {repo_name}: {e}")
        return

    # Fetch PR
    try:
        pr = repo.get_pull(pr_number)
    except Exception as e:
        print(f"Error fetching PR #{pr_number}: {e}")
        return

    changed_files = pr.get_files()
    print(f"Changed files in PR #{pr_number}:")

    for f in changed_files:
        print(f"- {f.filename}")

        # Fetch file content from the PR branch
        try:
            file_content = repo.get_contents(f.filename, ref=pr.head.ref).decoded_content.decode()
        except Exception as e:
            file_content = ""
            print(f"Could not fetch content for {f.filename}: {e}")

        # Generate AI suggestion
        suggestion = get_ai_suggestion(file_content, f.filename, or_key)

        # Post suggestion as PR comment
        pr.create_issue_comment(f"**AI Suggestion for {f.filename}:**\n{suggestion}")
        print(f"Posted AI suggestion for {f.filename}")

    print(f"\nAll AI suggestions posted to PR #{pr_number} successfully!")

if __name__ == "__main__":
    main()
