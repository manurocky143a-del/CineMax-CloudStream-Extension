import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
        print("Navigating to net77.cc/home...")
        await page.goto('https://net77.cc/home', wait_until='domcontentloaded')
        
        # Wait a bit for Cloudflare
        await page.wait_for_timeout(5000)
        
        print("Executing JS fetch for post.php...")
        # Execute the fetch directly in the page context
        js_code = """
        async () => {
            const t = Math.floor(Date.now() / 1000);
            const response = await fetch(`/post.php?id=70143836&t=${t}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            return await response.text();
        }
        """
        result = await page.evaluate(js_code)
        print("Result:", result)
            
        await browser.close()

asyncio.run(main())
