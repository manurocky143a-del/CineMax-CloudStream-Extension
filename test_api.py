import urllib.request
import time
import json

def fetch_bypass():
    req = urllib.request.Request('https://net77.cc/tv/p.php', data=b'', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        text = resp.read().decode()
        cookie = resp.info().get("Set-Cookie")
        print(f"[tv/p.php] -> {text}")
        print(f"[COOKIE] -> {cookie}")
        return cookie
    except Exception as e:
        print(f"[tv/p.php ERROR] -> {e}")
        return None

def test_api(url, cookie_str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://net77.cc/',
        'Cookie': cookie_str
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        print(f"[OK] {url}")
        return resp.read().decode()
    except Exception as e:
        print(f"[Error] {url} -> {e}")
    return None

c = fetch_bypass()
if c:
    cookie_str = c.split(';')[0]
    t = int(time.time())
    
    print("\n--- Search API ---")
    print(test_api(f'https://net77.cc/search.php?s=batman&t={t}', cookie_str))
    
    print("\n--- Details API (Batman Begins: 70021642) ---")
    post_res = test_api(f'https://net77.cc/post.php?id=70021642&t={t}', cookie_str)
    print(post_res)
    
    print("\n--- Episodes API (Breaking Bad: 70143836) ---")
    print(test_api(f'https://net77.cc/post.php?id=70143836&t={t}', cookie_str))
    
    print("\n--- Play API (Batman Begins: 70021642) ---")
    req_play = urllib.request.Request('https://net77.cc/play.php', data=b'id=70021642', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://net77.cc/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie_str
    })
    try:
        resp_play = urllib.request.urlopen(req_play, timeout=5)
        print("[play.php] -> " + resp_play.read().decode())
    except Exception as e:
        print(f"[play.php ERROR] -> {e}")
