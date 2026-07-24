import os

def replace_in_files(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.kt'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content.replace('com.horis.cloudstreamplugins', 'com.cinemax.cloudstreamplugins')
                new_content = new_content.replace('NetflixMirrorProvider', 'CineMaxProvider')
                new_content = new_content.replace('NetflixMirrorStorage', 'CineMaxStorage')
                new_content = new_content.replace('CNCVersePlugin', 'CineMaxPlugin')
                new_content = new_content.replace('class Netflix', 'class CineMax')
                new_content = new_content.replace('object Netflix', 'object CineMax')
                
                # Also replace display name in CineMaxProvider
                if f == 'CineMaxProvider.kt':
                    new_content = new_content.replace('override var name = "Netflix"', 'override var name = "CineMax"')

                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated {path}")

if __name__ == "__main__":
    replace_in_files(r"C:\Users\maxma\.gemini\antigravity\scratch\CineMax\CineMax\src\main\kotlin\com\cinemax\cloudstreamplugins")
