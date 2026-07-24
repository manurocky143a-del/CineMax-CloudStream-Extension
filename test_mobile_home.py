import urllib.request

req = urllib.request.Request('https://net77.cc/mobile/home', headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=5)
    print(f'[OK] -> {resp.status}')
    cookie = resp.info().get('Set-Cookie')
    print(f'[Cookie] -> {cookie}')
except Exception as e:
    print(f'[Error] -> {e}')
