import urllib.request
import json

def doh_lookup(domain):
    url = f"https://dns.google/resolve?name={domain}&type=A"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"DoH Lookup for {domain}:")
            answers = data.get("Answer", [])
            for a in answers:
                print(f"  Type {a['type']}: {a['data']}")
            return [a['data'] for a in answers if a['type'] == 1]
    except Exception as e:
        print(f"DoH Error for {domain}: {e}")
        return []

doh_lookup("s21.nm-cdn4.top")
doh_lookup("s20.nm-cdn.top")
doh_lookup("net77.cc")
