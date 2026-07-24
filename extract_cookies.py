import json

with open(r'C:\Users\maxma\Downloads\net77.cc.har', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for entry in data['log']['entries']:
        if 'net77.cc' in entry['request']['url']:
            if 'cookies' in entry['response']:
                for c in entry['response']['cookies']:
                    print(f"URL: {entry['request']['url']} | Set-Cookie: {c['name']} = {c['value']}")
