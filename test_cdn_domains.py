import urllib.request
import socket

# Test different CDN domain replacements for child m3u8:
# Original: https://s21.nm-cdn4.top/files/220884/720p/720p.m3u8?in=...
# Audio: https://s20.nm-cdn.top/files/70021642/a/0/0.m3u8

path = "/files/220884/720p/720p.m3u8?in=144c9defac04969c7bfad8efaa8ea194::5d0e6de44e5b6e00547dd61aeb7d58ee::1784905337::ni"

candidate_hosts = [
    "https://net77.cc",
    "https://back01.nfmirrorcdn.top",
    "https://subs.nfmirrorcdn.top",
    "https://img.nfmirrorcdn.top",
    "https://cdn.nfmirrorcdn.top",
    "https://s20.nfmirrorcdn.top",
    "https://s21.nfmirrorcdn.top"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://net77.cc/"
}

for host in candidate_hosts:
    url = host + path
    print("Testing URL:", url)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"SUCCESS! Status: {resp.status} | Size: {len(resp.read())}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} for {url}")
    except Exception as e:
        print(f"Error: {e} for {url}")
