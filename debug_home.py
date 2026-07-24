import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print("Navigating to https://net77.cc/home ...")
        response = await page.goto("https://net77.cc/home", wait_until="domcontentloaded", timeout=60000)
        print("Status:", response.status if response else "No response")
        
        # Wait up to 10 seconds for Cloudflare turnstile or page rendering
        await page.wait_for_timeout(10000)
        
        title = await page.title()
        print("Title:", title)
        
        content = await page.content()
        with open("net77_solved_home.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Cookies:")
        cookies = await context.cookies()
        for c in cookies:
            print(f"  {c['name']} = {c['value']}")

        await browser.close()

asyncio.run(main())
