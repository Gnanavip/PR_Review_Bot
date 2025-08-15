import os

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
    # Your bot logic goes here
    print("Tokens loaded successfully. Bot is running...")

if __name__ == "__main__":
    main()
