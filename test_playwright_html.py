import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
        await page.goto('https://net77.cc/home', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        html = await page.content()
        with open('net77_home.html', 'w', encoding='utf-8') as f:
            f.write(html)
            
        await browser.close()

asyncio.run(main())
