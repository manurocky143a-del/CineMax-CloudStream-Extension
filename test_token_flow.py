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

# Step 1: POST play.php
play_url = f"{mainUrl}/play.php"
play_data = urllib.parse.urlencode({"id": "70021642"}).encode("utf-8")

print("1. Requesting play.php...")
req1 = urllib.request.Request(play_url, data=play_data, headers=headers)
with urllib.request.urlopen(req1) as resp1:
    res1_text = resp1.read().decode("utf-8")
    print("play.php response:", res1_text)
    token_json = json.loads(res1_text)
    token = token_json.get("h", "")

print("\nExtracted Token 'h':", token)

# Step 2: Request playlist.php
playlist_url = f"{mainUrl}/playlist.php?id=70021642&t=Batman%20Begins&tm={t}"
print("\n2. Requesting playlist.php...")
req2 = urllib.request.Request(playlist_url, headers=headers)
with urllib.request.urlopen(req2) as resp2:
    playlist_res = resp2.read().decode("utf-8")
    print("playlist.php raw output:")
    print(playlist_res[:500])
    playlist = json.loads(playlist_res)

# Let's inspect the files in playlist
sources = playlist[0]["sources"]
for s in sources:
    raw_file = s["file"]
    print("\nSource file from playlist.php:", raw_file)
    
    # Replace in=unknown::ni with actual token if token is present
    if "in=unknown::ni" in raw_file and token:
        valid_file = raw_file.replace("in=unknown::ni", token)
    else:
        valid_file = raw_file
        
    full_url = mainUrl + valid_file if valid_file.startswith("/") else valid_file
    print("Modified Full HLS URL:", full_url)
    
    # Fetch master m3u8
    hls_req = urllib.request.Request(full_url, headers={"User-Agent": headers["User-Agent"], "Referer": "https://net77.cc/"})
    try:
        with urllib.request.urlopen(hls_req) as hls_resp:
            m3u8_content = hls_resp.read().decode("utf-8")
            print("Master M3U8 Content:\n", m3u8_content[:500])
            
            # Check child links inside master m3u8
            lines = [l.strip() for l in m3u8_content.splitlines() if l.strip() and not l.startswith("#")]
            for l in lines:
                print("\nChild URL inside m3u8:", l)
                try:
                    child_req = urllib.request.Request(l, headers={"User-Agent": headers["User-Agent"], "Referer": "https://net77.cc/"})
                    with urllib.request.urlopen(child_req) as child_resp:
                        print("Child M3U8 HTTP Status:", child_resp.status)
                        print("Child M3U8 Content (first 200 chars):", child_resp.read().decode("utf-8")[:200])
                except Exception as ce:
                    print("Error loading child URL:", ce)
    except Exception as e:
        print("Error loading master m3u8:", e)
