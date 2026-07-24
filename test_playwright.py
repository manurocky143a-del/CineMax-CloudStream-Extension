import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Intercept network requests
        page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: print("<<", response.status, response.url))
        
        print("Navigating to Breaking Bad...")
        await page.goto('https://net77.cc/show/70143836', wait_until='networkidle')
        
        # Wait a bit for Cloudflare and AJAX requests
        await page.wait_for_timeout(10000)
        
        print("Cookies:")
        cookies = await page.context.cookies()
        for cookie in cookies:
            print(cookie)
            
        await browser.close()

asyncio.run(main())
