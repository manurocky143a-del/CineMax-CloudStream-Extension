import os

def update_gradle_files(base_dir):
    # Root build.gradle.kts
    root_gradle = os.path.join(base_dir, "build.gradle.kts")
    with open(root_gradle, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('setRepo(System.getenv("GITHUB_REPOSITORY") ?: "https://github.com/NivinCNC/CNCVerse-Cloud-Stream-Extension")', 'setRepo(System.getenv("GITHUB_REPOSITORY") ?: "https://github.com/CineMax/CineMax-CloudStream")')
    content = content.replace('authors = listOf("NivinCNC")', 'authors = listOf("CineMax Devs")')
    content = content.replace('namespace = "com.cncverse"', 'namespace = "com.cinemax"')
    with open(root_gradle, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # Subproject build.gradle.kts
    sub_gradle = os.path.join(base_dir, "CineMax", "build.gradle.kts")
    with open(sub_gradle, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('version = 24', 'version = 1')
    content = content.replace('description = "Netflix, PrimeVideo, Disney+ Hotstar Contents in Multiple Languages"', 'description = "An independent CloudStream extension for CineMax"')
    content = content.replace('authors = listOf("NivinCNC")', 'authors = listOf("CineMax Devs")')
    content = content.replace('iconUrl = "https://github.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/raw/refs/heads/master/CNC%20Verse/icon.png"', 'iconUrl = ""')
    
    with open(sub_gradle, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_gradle_files(r"C:\Users\maxma\.gemini\antigravity\scratch\CineMax")
