import json

with open(r'C:\Users\maxma\Downloads\net77.cc.har', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for entry in data['log']['entries']:
        if 'post.php' in entry['request']['url']:
            print(entry['request']['url'])
            for h in entry['request']['headers']:
                print(f"{h['name']}: {h['value']}")
            print('-' * 20)
            break
