import urllib.request
import json
import time

BASE_URL = "https://net77.cc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://net77.cc/",
    "X-Requested-With": "XMLHttpRequest"
}

t = int(time.time())

endpoints = [
    f"/search.php?s=&t={t}",
    f"/search.php?s=a&t={t}",
    f"/search.php?s=2024&t={t}",
    f"/search.php?s=action&t={t}",
    f"/search.php?s=movie&t={t}",
    f"/trays.php?t={t}",
    f"/trending.php?t={t}",
    f"/top.php?t={t}",
    f"/home.php?t={t}",
    f"/list.php?t={t}",
    f"/index.php?t={t}",
    f"/category.php?t={t}",
]

for ep in endpoints:
    url = BASE_URL + ep
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            print(f"URL: {ep} | Code: {resp.status} | Size: {len(data)} | Body preview: {data[:150]}")
    except Exception as e:
        print(f"URL: {ep} | Error: {e}")
