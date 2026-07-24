import os

def check_references(directory):
    bad_strings = ["horis", "NetflixMirrorProvider", "NetflixMirrorStorage", "CNCVerse"]
    found_issues = False
    
    for root, dirs, files in os.walk(directory):
        if ".git" in root or "build" in root or "gradle" in root:
            continue
        for f in files:
            if f.endswith('.kt') or f.endswith('.kts') or f.endswith('.md'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    try:
                        content = file.read()
                        for b in bad_strings:
                            if b.lower() in content.lower():
                                print(f"Found {b} in {path}")
                                found_issues = True
                    except Exception as e:
                        pass
                        
    if not found_issues:
        print("Verification passed! No bad references found in code.")

if __name__ == "__main__":
    check_references(r"C:\Users\maxma\.gemini\antigravity\scratch\CineMax")
