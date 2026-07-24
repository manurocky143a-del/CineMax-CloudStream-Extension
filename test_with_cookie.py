import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Intercept XHR / Fetch
        page.on("response", lambda res: print(f"FETCH [{res.status}] {res.url}"))
        
        print("Navigating to net77.cc...")
        await page.goto("https://net77.cc/", wait_until="domcontentloaded")
        await page.wait_for_timeout(10000)
        
        # Navigate to /home now that clearance should be active
        print("Navigating to net77.cc/home...")
        await page.goto("https://net77.cc/home", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        
        title = await page.title()
        print("Page Title:", title)
        
        content = await page.content()
        with open("net77_actual_home.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        # Check elements
        trays = await page.query_selector_all(".tray-container, #top10, article, .top10-post")
        print(f"Found {len(trays)} tray/item elements in DOM!")
        
        # Also test fetch post.php from page context
        t = 1784904305
        post_res = await page.evaluate(f"fetch('/post.php?id=70021642&t={t}', {{headers: {{'X-Requested-With': 'XMLHttpRequest'}}}}).then(r => r.text())")
        print("post.php result from inside page:", post_res[:300])

        await browser.close()

asyncio.run(main())
