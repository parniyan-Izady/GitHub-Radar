"""GitHub Relationship Radar - Backend Server

A lightweight, zero-dependency local HTTP server providing:
1. Static hosting for the frontend web application.
2. REST API endpoint (/api/analyze) to query GitHub followers and following lists.
"""

import http.server
import json
import os
import socketserver
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Tuple

PORT: int = 8000
DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))


class GitHubRadarHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler to serve UI and proxy GitHub requests."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self) -> None:
        """Handle incoming GET requests."""
        if self.path.startswith("/api/analyze"):
            self.handle_analyze()
        elif self.path in ("/", ""):
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def handle_analyze(self) -> None:
        """Analyze GitHub followers vs following for target user."""
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)

        raw_user = params.get("user", [""])[0].strip()
        token = params.get("token", [""])[0].strip()

        # Sanitize username or handle profile URL
        user = raw_user.rstrip("/").split("/")[-1]

        if not user:
            self.send_json_response(400, {"error": "Target username is required."})
            return

        headers = {
            "User-Agent": "GitHub-Unfollower-Radar",
            "Accept": "application/vnd.github.v3+json",
        }
        if token:
            headers["Authorization"] = f"token {token}"

        try:
            profile = self.fetch_json(f"https://api.github.com/users/{user}", headers)
            followers = self.fetch_all_pages(
                f"https://api.github.com/users/{user}/followers", headers
            )
            following = self.fetch_all_pages(
                f"https://api.github.com/users/{user}/following", headers
            )

            follower_logins = {u["login"].lower(): u for u in followers}
            following_logins = {u["login"].lower(): u for u in following}

            not_following_back = [
                u for u in following if u["login"].lower() not in follower_logins
            ]
            fans = [
                u for u in followers if u["login"].lower() not in following_logins
            ]
            mutual = [
                u for u in following if u["login"].lower() in follower_logins
            ]

            payload = {
                "profile": profile,
                "counts": {
                    "followers": len(followers),
                    "following": len(following),
                    "not_following_back": len(not_following_back),
                    "fans": len(fans),
                    "mutual": len(mutual),
                },
                "unfollowers": not_following_back,
                "fans": fans,
                "mutual": mutual,
            }
            self.send_json_response(200, payload)

        except urllib.error.HTTPError as err:
            try:
                err_data = json.loads(err.read().decode("utf-8"))
                msg = err_data.get("message", str(err))
            except Exception:
                msg = str(err)
            self.send_json_response(err.code, {"error": f"GitHub API error: {msg}"})

        except Exception as err:
            self.send_json_response(500, {"error": f"Internal error: {str(err)}"})

    def fetch_json(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Fetch a single JSON resource from GitHub API."""
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))

    def fetch_all_pages(
        self, base_url: str, headers: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Paginate through all items for a GitHub collection endpoint."""
        results: List[Dict[str, Any]] = []
        page = 1
        while True:
            url = f"{base_url}?per_page=100&page={page}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data:
                    break
                results.extend(data)
                if len(data) < 100:
                    break
                page += 1
        return results

    def send_json_response(self, code: int, data: Dict[str, Any]) -> None:
        """Helper to send JSON response with CORS headers."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    """Start the HTTP server on configured port."""
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), GitHubRadarHandler) as httpd:
        print("=" * 60)
        print(f"🚀 GitHub Radar running at: http://localhost:{PORT}")
        print("Press Ctrl+C to terminate.")
        print("=" * 60)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
