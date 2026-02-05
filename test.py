import re
def parse_repo(state:dict):
    text="https://github.com/mohithingorani/RAG-CHAIN-FOR-AI-ARTICLE"
    text = state.messages[0].content
    match = re.search(r"https?://github\.com/[^\s]+", text)
    if not match:
        return None

    url = match.group(0).rstrip("/")

    clean = re.sub(r"^https?://github\.com/", "", url)
    parts = clean.split("/")

    return {
        "owner": parts[0] if len(parts) > 0 else None,
        "repo": parts[1] if len(parts) > 1 else None,
        "llm_calls":0,
        "files":None,
        "messages":[],
        "path":""
    }

# repo = parse_github_repo_from_text("tell me about https://github.com/mohithingorani/RAG-CHAIN-FOR-AI-ARTICLE")
# print(repo)