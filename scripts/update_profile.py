"""Generate a local profile card using public GitHub data; no dependencies."""
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

USERNAME = "sheikhabdullah9july-commits"
ROOT = Path(__file__).resolve().parents[1]


def github(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Abdullah-Profile-Snapshot"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request("https://api.github.com/" + path, headers=headers), timeout=30) as response:
        return json.load(response)


def collect():
    profile = github("users/" + quote(USERNAME))
    repositories = []
    page = 1
    while True:
        batch = github(f"users/{quote(USERNAME)}/repos?type=owner&per_page=100&page={page}")
        repositories.extend(repo for repo in batch if not repo.get("private", False))
        if len(batch) < 100:
            break
        page += 1
    languages = {}
    for repo in repositories:
        language = repo.get("language")
        if language:
            languages[language] = languages.get(language, 0) + 1
    last_push = max((repo["pushed_at"] for repo in repositories if repo.get("pushed_at")), default=None)
    return {
        "username": USERNAME,
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "public_repositories": len(repositories),
        "stars_received": sum(repo.get("stargazers_count", 0) for repo in repositories),
        "followers": profile.get("followers", 0),
        "last_public_push": last_push[:10] if last_push else "No pushes yet",
        "primary_language_counts": dict(sorted(languages.items(), key=lambda pair: (-pair[1], pair[0]))),
    }


def render(data):
    languages = data["primary_language_counts"]
    language_label = " · ".join(f"{name} ({count})" for name, count in languages.items()) or "No public language data yet"
    # Long language inventories stay in JSON rather than overflowing the image.
    if len(language_label) > 105:
        language_label = " · ".join(f"{name} ({count})" for name, count in list(languages.items())[:5])
    metrics = [
        ("PUBLIC REPOSITORIES", data["public_repositories"], "#5ee6bd"),
        ("STARS RECEIVED", data["stars_received"], "#ffbd7a"),
        ("FOLLOWERS", data["followers"], "#d3b0ff"),
        ("LATEST PUBLIC PUSH", data["last_public_push"], "#96c7ff"),
    ]
    boxes = []
    for index, (label, value, color) in enumerate(metrics):
        x = 27 + index * 265
        size = 25 if index == 3 else 37
        boxes.append(f'<rect x="{x}" y="72" width="249" height="96" rx="11" fill="#182b3b"/>'
                     f'<text x="{x+18}" y="100" font-size="10" letter-spacing="1" fill="#a4bdce">{label}</text>'
                     f'<text x="{x+18}" y="145" font-size="{size}" font-weight="700" fill="{color}">{escape(str(value))}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="257" viewBox="0 0 1100 257" role="img" aria-labelledby="title desc">
<title id="title">M. Abdullah's public GitHub snapshot</title>
<desc id="desc">Public repositories: {data['public_repositories']}. Stars received: {data['stars_received']}. Followers: {data['followers']}. Updated {data['updated_utc']} UTC.</desc>
<rect width="1100" height="257" rx="16" fill="#101c2a"/>
<g font-family="Segoe UI,Arial,sans-serif">
<text x="28" y="42" font-size="19" font-weight="650" fill="#edf5fa">Public work, at a glance.</text>
<text x="1070" y="41" text-anchor="end" font-size="11" fill="#8aa8bb">Updated {data['updated_utc']} UTC</text>
{''.join(boxes)}
<text x="28" y="200" font-size="11" fill="#8aa8bb">PRIMARY LANGUAGES · NUMBER OF PUBLIC REPOSITORIES</text>
<text x="28" y="228" font-size="14" fill="#c4d8e6">{escape(language_label)}</text>
</g></svg>\n'''


def main():
    data = collect()
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "assets/github-snapshot.svg").write_text(render(data), encoding="utf-8")
    (ROOT / "data/public-snapshot.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Updated the public profile snapshot for " + USERNAME)


if __name__ == "__main__":
    main()
