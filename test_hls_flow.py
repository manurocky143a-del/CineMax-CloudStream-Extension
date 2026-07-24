import urllib.request
import json
import time

t = int(time.time())
mainUrl = "https://net77.cc"

# 1. Fetch playlist.php
playlistUrl = f"{mainUrl}/playlist.php?id=70021642&t=Batman%20Begins&tm={t}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://net77.cc/",
    "X-Requested-With": "XMLHttpRequest"
}

print("Fetching playlist:", playlistUrl)
req = urllib.request.Request(playlistUrl, headers=headers)
with urllib.request.urlopen(req) as resp:
    playlist_data = json.loads(resp.read().decode('utf-8'))

print("Playlist JSON:")
print(json.dumps(playlist_data, indent=2))

sources = playlist_data[0]["sources"]
for s in sources:
    raw_file = s["file"]
    full_url = mainUrl + raw_file if raw_file.startswith("/") else raw_file
    print("\n----------------------------------------")
    print(f"Source Label: {s['label']}")
    print(f"Raw File: {raw_file}")
    print(f"Full URL: {full_url}")
    
    # Test fetching master m3u8
    hls_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://net77.cc/",
        "Origin": "https://net77.cc"
    }
    
    hls_req = urllib.request.Request(full_url, headers=hls_headers)
    try:
        with urllib.request.urlopen(hls_req) as hls_resp:
            print("HLS HTTP Status:", hls_resp.status)
            print("HLS Final URL:", hls_resp.geturl())
            hls_body = hls_resp.read().decode('utf-8')
            print("HLS Body (first 400 chars):\n", hls_body[:400])
            
            # Extract first child m3u8 link from master playlist
            lines = [line.strip() for line in hls_body.splitlines() if line.strip() and not line.startswith('#')]
            if lines:
                child_m3u8 = lines[0]
                print("\nChild M3U8 Link found:", child_m3u8)
                child_req = urllib.request.Request(child_m3u8, headers=hls_headers)
                with urllib.request.urlopen(child_req) as child_resp:
                    print("Child M3U8 Status:", child_resp.status)
                    print("Child M3U8 Body (first 300 chars):\n", child_resp.read().decode('utf-8')[:300])
    except Exception as e:
        print("Error fetching HLS:", e)
