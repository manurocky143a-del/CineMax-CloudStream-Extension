import urllib.request
import urllib.parse
import json
import time

mainUrl = "https://net77.cc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://net77.cc/",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

t = int(time.time())

# Step 1: Get FRESH token from play.php
play_url = f"{mainUrl}/play.php"
play_data = urllib.parse.urlencode({"id": "70021642"}).encode("utf-8")
req1 = urllib.request.Request(play_url, data=play_data, headers=headers)
with urllib.request.urlopen(req1) as resp1:
    token = json.loads(resp1.read().decode("utf-8")).get("h", "")

print("FRESH TOKEN:", token)

# Step 2: Fetch Master M3U8 from net77.cc
master_url = f"{mainUrl}/hls/70021642.m3u8?in={token}"
print("Fetching Master M3U8:", master_url)
req2 = urllib.request.Request(master_url, headers={"User-Agent": headers["User-Agent"], "Referer": "https://net77.cc/"})
with urllib.request.urlopen(req2) as resp2:
    master_m3u8 = resp2.read().decode("utf-8")

print("\nMaster M3U8 Output:\n", master_m3u8)

# Extract child URL lines
child_urls = [line.strip() for line in master_m3u8.splitlines() if line.strip() and not line.startswith("#")]
print("\nChild URLs extracted from Master M3U8:")
for c in child_urls:
    print("  ", c)

# Test candidate domain replacements for each child URL
candidate_domains = [
    "https://net77.cc",
    "https://img.nfmirrorcdn.top",
    "https://subs.nfmirrorcdn.top",
    "https://back01.nfmirrorcdn.top"
]

for orig_url in child_urls:
    # extract path starting from /files/
    if "/files/" in orig_url:
        path = "/files/" + orig_url.split("/files/")[1]
    else:
        path = orig_url

    print(f"\nTesting path: {path}")
    for domain in candidate_domains:
        test_url = domain + path
        print(f"  Trying {test_url} ...")
        try:
            r = urllib.request.Request(test_url, headers={"User-Agent": headers["User-Agent"], "Referer": "https://net77.cc/"})
            with urllib.request.urlopen(r, timeout=5) as res:
                print(f"    SUCCESS! [{res.status}] Length: {len(res.read())}")
        except urllib.error.HTTPError as e:
            print(f"    HTTP Error {e.code}")
        except Exception as e:
            print(f"    Error: {e}")
