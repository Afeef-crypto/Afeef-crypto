#!/usr/bin/env python3
"""
update_readme.py
Fetches LeetCode stats, generates SVG cards, updates README markers.
"""

import re, sys, requests
import generate_cards as cards

# Profile: https://leetcode.com/u/mohammed_afeefuddin/
ACCOUNTS = {
    "MAIN":     "mohammed_afeefuddin",
    "CONTESTS": "mohammed_afeefuddin",
}
README_PATH  = "README.md"
LEETCODE_GQL = "https://leetcode.com/graphql"
RAW_BASE = "assets/cards"
# Absolute raw URLs so README images render on github.com/.../blob/... previews (relative paths often fail).
PROFILE_REPO = "Afeef-crypto/Afeef-crypto"
DEFAULT_BRANCH = "main"


def raw_asset_url(relative: str) -> str:
    return f"https://raw.githubusercontent.com/{PROFILE_REPO}/{DEFAULT_BRANCH}/{relative}"

HEADERS = {
    "Content-Type": "application/json",
    "Referer":      "https://leetcode.com",
    "User-Agent":   "Mozilla/5.0",
}

PROFILE_QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    submitStats { acSubmissionNum { difficulty count } }
  }
}
"""

CONTEST_QUERY = """
query getUserContestRanking($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    topPercentage
  }
}
"""

def gql(query, variables):
    r = requests.post(LEETCODE_GQL, json={"query": query, "variables": variables},
                      headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_main(username):
    data  = gql(PROFILE_QUERY, {"username": username})
    user  = data["data"]["matchedUser"]
    stats = {s["difficulty"]: s for s in user["submitStats"]["acSubmissionNum"]}
    return {
        "username": user["username"],
        "total":    stats.get("All",    {}).get("count", 0),
        "easy":     stats.get("Easy",   {}).get("count", 0),
        "medium":   stats.get("Medium", {}).get("count", 0),
        "hard":     stats.get("Hard",   {}).get("count", 0),
    }

def fetch_contests(username):
    p  = gql(PROFILE_QUERY,  {"username": username})
    c  = gql(CONTEST_QUERY,  {"username": username})
    user  = p["data"]["matchedUser"]
    stats = {s["difficulty"]: s for s in user["submitStats"]["acSubmissionNum"]}
    cr    = c["data"].get("userContestRanking") or {}
    return {
        "username":       user["username"],
        "total":          stats.get("All",    {}).get("count", 0),
        "easy":           stats.get("Easy",   {}).get("count", 0),
        "medium":         stats.get("Medium", {}).get("count", 0),
        "hard":           stats.get("Hard",   {}).get("count", 0),
        "rating":         int(cr.get("rating") or 0),
        "global_rank":    cr.get("globalRanking") or 0,
        "top_pct":        round(float(cr.get("topPercentage") or 0), 1),
        "contests_count": cr.get("attendedContestsCount") or 0,
    }

def leetcode_profile_url(username):
    return f"https://leetcode.com/u/{username}/"

def img_block(png_file, username, alt):
    link = leetcode_profile_url(username)
    src = raw_asset_url(f"{RAW_BASE}/{png_file}")
    return (
        f'<div align="center">\n'
        f'  <a href="{link}">\n'
        f'    <img src="{src}" alt="{alt}" width="520" />\n'
        f'  </a>\n'
        f'</div>\n'
    )

def replace_section(content, marker, body):
    pat = rf"(<!-- {marker}:START -->).*?(<!-- {marker}:END -->)"
    return re.sub(pat, rf"\1\n{body}\2", content, flags=re.DOTALL)

def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    try:
        d = fetch_main(ACCOUNTS["MAIN"])
        cards.write_main(d)
        content = replace_section(content, "LEETCODE-MAIN",
            img_block("lc_main.png", d["username"], "LeetCode main stats"))
        print(f"[ok] Main ({d['username']}): {d['total']} solved")
    except Exception as e:
        errors.append(str(e))
        print(f"[err] Main failed: {e}", file=sys.stderr)

    try:
        d = fetch_contests(ACCOUNTS["CONTESTS"])
        cards.write_contests(d)
        content = replace_section(content, "LEETCODE-CONTESTS",
            img_block("lc_contests.png", d["username"], "LeetCode contests"))
        print(f"[ok] Contests ({d['username']}): {d['total']} solved, rating {d['rating']}")
    except Exception as e:
        errors.append(str(e))
        print(f"[err] Contests failed: {e}", file=sys.stderr)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[ok] README.md written")

    if errors:
        print(f"\n[warn] {len(errors)} error(s)")
        sys.exit(1)

if __name__ == "__main__":
    main()
