import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test fetching via IP 207.207.210.229 with Host header s21.nm-cdn4.top
ip = "207.207.210.229"
token_path = "/files/220884/720p/720p.m3u8?in=144c9defac04969c7bfad8efaa8ea194::5d0e6de44e5b6e00547dd61aeb7d58ee::1784905337::ni"

url = f"https://{ip}{token_path}"
headers = {
    "Host": "s21.nm-cdn4.top",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://net77.cc/"
}

print("Testing direct IP fetch:", url)
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        print("Status:", resp.status)
        body = resp.read().decode('utf-8', errors='ignore')
        print("Response body:\n", body[:400])
except Exception as e:
    print("Error:", e)
