import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        page.on("request", lambda request: print(f">> {request.method} {request.url}") if request.resource_type in ["fetch", "xhr"] else None)
        
        async def handle_response(response):
            if response.request.resource_type in ["fetch", "xhr"]:
                try:
                    text = await response.text()
                    print(f"<< {response.status} {response.url} -> {text[:200]}")
                except:
                    pass
        page.on("response", handle_response)
        
        print("Navigating to net77.cc/home...")
        await page.goto('https://net77.cc/home', wait_until='domcontentloaded')
        await page.wait_for_timeout(10000)
        
        print("Clicking a random movie on homepage...")
        # find the first element that looks like a movie link or card and click it
        js_click = """
        () => {
            const el = document.querySelector('[data-post], .card-img-container, .top10-post, .tray-item');
            if (el) {
                el.click();
                return "Clicked " + el.className;
            }
            return "No element found";
        }
        """
        res = await page.evaluate(js_click)
        print(res)
        
        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(main())
