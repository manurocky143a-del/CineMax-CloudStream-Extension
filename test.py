import urllib.request, json
url = 'https://api.github.com/repos/recloudstream/cloudstream/releases'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req).read()
    releases = json.loads(resp)
    for r in releases:
        has_classes = any(a['name'] == 'classes.jar' for a in r.get('assets', []))
        if has_classes:
            print(f"{r['tag_name']} has classes.jar")
except Exception as e:
    print('Error:', e)
