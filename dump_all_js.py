import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://net77.cc/home", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        scripts = await page.evaluate("""
        () => Array.from(document.querySelectorAll('script')).map(s => s.src ? {type: 'src', content: s.src} : {type: 'inline', content: s.innerHTML})
        """)

        print(f"Total scripts found: {len(scripts)}")
        for idx, s in enumerate(scripts):
            print(f"=== SCRIPT {idx} ({s['type']}) ===")
            print(s['content'][:500])
            print("\n")

        await browser.close()

asyncio.run(main())
