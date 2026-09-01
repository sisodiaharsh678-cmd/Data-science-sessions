"""
Step 1: Fetch documentation from a GitHub repo (README + docs folder)
Usage: python fetch_repo_docs.py
"""

import requests
import os
import base64
import json

# ---- CONFIG ----
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")  # set this as an env var, don't hardcode
REPO_OWNER = "sisodiaharsh678-cmd"
REPO_NAME = "alzheimer-app"
OUTPUT_DIR = "raw_docs"

HEADERS = {
    "Accept": "application/vnd.github+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def fetch_readme():
    """Fetch the README.md content from the repo. Returns None if no README exists."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/readme"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 404:
        print("No README.md found in this repo - skipping (this is fine, not an error).")
        return None
    resp.raise_for_status()
    data = resp.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content


def fetch_repo_tree():
    """Get the full file tree of the repo (to find docs, code files, etc)."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/main?recursive=1"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get("tree", [])


def fetch_file_content(path):
    """Fetch raw content of a specific file path in the repo."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if "content" in data:
        return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return ""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Fetching README from {REPO_OWNER}/{REPO_NAME}...")
    readme = fetch_readme()
    if readme:
        with open(f"{OUTPUT_DIR}/README.md", "w") as f:
            f.write(readme)
        print(f"Saved README.md ({len(readme)} chars)")

    print("Fetching repo file tree...")
    tree = fetch_repo_tree()

    # Pull markdown files and Python files (docstrings/comments carry useful info)
    relevant_files = [
        item["path"] for item in tree
        if item["type"] == "blob" and (item["path"].endswith(".md") or item["path"].endswith(".py"))
    ]
    print(f"Found {len(relevant_files)} relevant files: {relevant_files}")

    for path in relevant_files:
        if path == "README.md":
            continue  # already fetched
        try:
            content = fetch_file_content(path)
            safe_name = path.replace("/", "__")
            with open(f"{OUTPUT_DIR}/{safe_name}", "w") as f:
                f.write(content)
            print(f"Saved {path} ({len(content)} chars)")
        except Exception as e:
            print(f"Skipped {path}: {e}")

    print("\nDone. All docs saved to ./raw_docs/")


if __name__ == "__main__":
    main()