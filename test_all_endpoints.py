import urllib.request
import json
import time

BASE_URL = "https://net77.cc"

headers_base = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://net77.cc/",
    "X-Requested-With": "XMLHttpRequest"
}

def test_endpoint(name, url, method="GET", data=None, extra_headers=None):
    print("==================================================")
    print(f"TEST: {name}")
    print(f"URL: {url}")
    headers = headers_base.copy()
    if extra_headers:
        headers.update(extra_headers)
    print(f"Headers: {headers}")
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            cookies = resp.headers.get_all("Set-Cookie")
            body = resp.read().decode('utf-8', errors='ignore')
            print(f"HTTP Status: {status}")
            print(f"Cookies: {cookies}")
            print(f"Body (first 500 chars):\n{body[:500]}")
            return status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error: {e.code}")
        print(f"Body (first 500 chars):\n{body[:500]}")
        return e.code, body
    except Exception as e:
        print(f"Exception: {e}")
        return None, str(e)

t = int(time.time())

# 1. Main Page / Home
test_endpoint("Home Page", f"{BASE_URL}/home")

# 2. Search API
test_endpoint("Search API", f"{BASE_URL}/search.php?s=batman&t={t}")

# 3. Mini Modal Info
test_endpoint("Mini Modal Info", f"{BASE_URL}/mini-modal-info.php?id=70021642&t={t}")

# 4. Post API (Movie details)
test_endpoint("Post API", f"{BASE_URL}/post.php?id=70021642&t={t}")

# 5. Play API
test_endpoint("Play API", f"{BASE_URL}/play.php", method="POST", data=f"id=70021642".encode('utf-8'), extra_headers={"Content-Type": "application/x-www-form-urlencoded"})

# 6. Playlist API
test_endpoint("Playlist API", f"{BASE_URL}/playlist.php?id=70021642&t=Batman%20Begins&tm={t}")

