import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch headful browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Navigating to net77.cc...")
        await page.goto("https://net77.cc/home", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        # Click first movie card to open modal/player
        print("Clicking a movie card...")
        await page.evaluate("""
        () => {
            const card = document.querySelector('[data-post]');
            if (card) card.click();
        }
        """)
        await page.wait_for_timeout(5000)

        # Find play button inside modal or page and click it
        print("Clicking play button...")
        await page.evaluate("""
        () => {
            const btn = document.querySelector('.play-btn, .btn-play, [onclick*="play"], #playBtn');
            if (btn) btn.click();
        }
        """)
        await page.wait_for_timeout(10000)

        # Inspect frames / video element / script source
        scripts = await page.evaluate("""
        () => Array.from(document.querySelectorAll('script')).map(s => s.src || s.innerHTML).filter(s => s.includes('playlist') || s.includes('nm-cdn') || s.includes('hls'))
        """)
        print("Player scripts found:", len(scripts))
        for idx, s in enumerate(scripts[:5]):
            print(f"--- Script {idx} ---")
            print(s[:400])

        await browser.close()

asyncio.run(main())
