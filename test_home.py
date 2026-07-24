import urllib.request
import re

req = urllib.request.Request('https://net77.cc/home', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})
try:
    resp = urllib.request.urlopen(req, timeout=5)
    html = resp.read().decode()
    cookie = resp.info().get('Set-Cookie')
    print(f'[Cookie] -> {cookie}')
    matches = re.findall(r't_hash_t.*', html)
    print(f'[JS Hash] -> {matches}')
except Exception as e:
    print(f'[Error] -> {e}')
