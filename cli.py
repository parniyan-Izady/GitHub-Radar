"""GitHub Relationship Radar - Command Line Interface (CLI)

Run via:
    python cli.py <username> [--token <TOKEN>] [--csv <FILENAME>]
"""

import argparse
import csv
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List


def fetch_all(base_url: str, token: str = "") -> List[Dict[str, Any]]:
    """Fetch all pages from a GitHub collection endpoint with 20s timeout."""
    headers = {
        "User-Agent": "GitHub-Radar-CLI",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    results: List[Dict[str, Any]] = []
    page = 1
    while True:
        url = f"{base_url}?per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data:
                    break
                results.extend(data)
                if len(data) < 100:
                    break
                page += 1
        except urllib.error.HTTPError as err:
            print(f"[!] HTTP Error {err.code}: {err.reason}", file=sys.stderr)
            break
        except Exception as err:
            print(f"[!] Error: {err}", file=sys.stderr)
            break
    return results


def run_cli() -> None:
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Inspect GitHub followers, non-mutual follows, and admirers."
    )
    parser.add_argument(
        "username",
        help="GitHub username or profile URL",
    )
    parser.add_argument(
        "--token",
        default="",
        help="GitHub Personal Access Token for higher rate limits (5,000 req/hr)",
    )
    parser.add_argument(
        "--csv",
        default="",
        help="Path to export not-following-back list to CSV",
    )
    args = parser.parse_args()

    clean_user = args.username.rstrip("/").split("/")[-1]
    print(f"\nScanning relationship status for @{clean_user}...\n")

    followers_list = fetch_all(f"https://api.github.com/users/{clean_user}/followers", args.token)
    following_list = fetch_all(f"https://api.github.com/users/{clean_user}/following", args.token)

    followers_map = {u["login"].lower(): u for u in followers_list}
    following_map = {u["login"].lower(): u for u in following_list}

    not_following_back = [u for u in following_list if u["login"].lower() not in followers_map]
    fans = [u for u in followers_list if u["login"].lower() not in following_map]
    mutual = [u for u in following_list if u["login"].lower() in followers_map]

    print("=" * 60)
    print(f"🛰️  GitHub Summary for @{clean_user}")
    print("=" * 60)
    print(f" Followers : {len(followers_list):,}")
    print(f" Following : {len(following_list):,}")
    print(f" Mutual    : {len(mutual):,}")
    print("-" * 60)
    print(f" ❌ Followed by @{clean_user} but NOT following back: {len(not_following_back):,}")
    print(f" ⭐ Following @{clean_user} but NOT followed back    : {len(fans):,}")
    print("=" * 60)

    if not_following_back:
        print(f"\nTop users who do NOT follow back (showing up to 20):")
        for user in not_following_back[:20]:
            print(f"  - @{user['login']:<20} -> {user['html_url']}")
        if len(not_following_back) > 20:
            print(f"  ... and {len(not_following_back) - 20} more.")

    if args.csv and not_following_back:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "profile_url", "avatar_url"])
            for u in not_following_back:
                writer.writerow([u["login"], u["html_url"], u["avatar_url"]])
        print(f"\n[+] Exported non-followers to: {args.csv}")


if __name__ == "__main__":
    run_cli()
