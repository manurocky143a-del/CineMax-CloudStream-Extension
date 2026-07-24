import socket
import urllib.request

domains = [
    "s21.nm-cdn4.top",
    "s20.nm-cdn.top",
    "nm-cdn4.top",
    "nm-cdn.top",
    "nfmirrorcdn.top",
    "img.nfmirrorcdn.top",
    "subs.nfmirrorcdn.top"
]

for d in domains:
    try:
        ip = socket.gethostbyname(d)
        print(f"Domain: {d} -> IP: {ip}")
    except Exception as e:
        print(f"Domain: {d} -> DNS Lookup Failed: {e}")
