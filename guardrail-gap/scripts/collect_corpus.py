import requests
import json
import time
import csv
import base64
from datetime import datetime

# Using unauthenticated public GitHub search (60 req/hr limit, good for demo)
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

VIBE_QUERIES = [
    '"vibe coding" in:readme',
    '"vibe coded" in:readme',
    '"built with AI" in:readme language:python',
    '"built with AI" in:readme language:javascript',
]

OPEN_WEIGHT_SIGNALS = [
    "ollama", "lm studio", "llama.cpp", "llama3", "llama-3",
    "mistral", "qwen", "deepseek", "phi-3", "phi3",
    "gemma", "open-webui", "openwebui", "localai"
]

PROPRIETARY_SIGNALS = [
    "lovable.dev", "bolt.new", "replit agent", "github copilot",
    "cursor", "gpt-4", "gpt4", "claude", "gemini", "chatgpt"
]

def search_repos(query, max_results=30):
    repos = []
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "updated", "order": "desc", "per_page": min(30, max_results)}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if resp.status_code == 200:
            repos = resp.json().get("items", [])
        elif resp.status_code == 403:
            print(f"  Rate limited on query: {query}")
    except Exception as e:
        print(f"  Error: {e}")
    time.sleep(1)
    return repos[:max_results]

def get_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code == 200:
            content = resp.json().get("content", "")
            return base64.b64decode(content).decode("utf-8", errors="ignore")
    except Exception:
        pass
    return ""

def classify_model_type(readme_text):
    readme_lower = readme_text.lower()
    open_score = sum(1 for s in OPEN_WEIGHT_SIGNALS if s in readme_lower)
    prop_score = sum(1 for s in PROPRIETARY_SIGNALS if s in readme_lower)
    if open_score > 0 and prop_score == 0:
        return "open_weight", open_score
    elif prop_score > 0 and open_score == 0:
        return "proprietary", prop_score
    elif open_score > 0 and prop_score > 0:
        return "mixed", max(open_score, prop_score)
    return "unknown", 0

all_repos = []
seen = set()

for query in VIBE_QUERIES:
    print(f"Searching: {query}")
    repos = search_repos(query, max_results=25)
    for r in repos:
        full_name = r.get("full_name", "")
        if not full_name or full_name in seen:
            continue
        seen.add(full_name)
        owner, name = full_name.split("/", 1)
        readme = get_readme(owner, name)
        model_type, signal_count = classify_model_type(readme)
        all_repos.append({
            "full_name": full_name,
            "url": r.get("html_url", ""),
            "clone_url": r.get("clone_url", ""),
            "language": r.get("language", ""),
            "stars": r.get("stargazers_count", 0),
            "created_at": r.get("created_at", ""),
            "updated_at": r.get("updated_at", ""),
            "model_type": model_type,
            "signal_count": signal_count,
            "size_kb": r.get("size", 0),
        })
        time.sleep(0.3)
    print(f"  Found {len(repos)} repos so far...")
    time.sleep(2)

with open("/home/claude/corpus.csv", "w", newline="") as f:
    if all_repos:
        writer = csv.DictWriter(f, fieldnames=all_repos[0].keys())
        writer.writeheader()
        writer.writerows(all_repos)

print(f"\nTotal collected: {len(all_repos)}")
print(f"Open-weight:  {sum(1 for r in all_repos if r['model_type'] == 'open_weight')}")
print(f"Proprietary:  {sum(1 for r in all_repos if r['model_type'] == 'proprietary')}")
print(f"Mixed:        {sum(1 for r in all_repos if r['model_type'] == 'mixed')}")
print(f"Unknown:      {sum(1 for r in all_repos if r['model_type'] == 'unknown')}")
