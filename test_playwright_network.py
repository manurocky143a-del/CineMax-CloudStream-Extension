import asyncio
from playwright.async_api import async_playwright
import urllib.request
import json
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
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
        await page.wait_for_timeout(5000)
        
        t = int(time.time())
        print("Searching for breaking bad...")
        js_search = f"""
        async () => {{
            const response = await fetch(`/search.php?s=breaking&t={t}`, {{ headers: {{ 'X-Requested-With': 'XMLHttpRequest' }} }});
            return await response.text();
        }}
        """
        res = await page.evaluate(js_search)
        data = json.loads(res)
        first_id = data['searchResult'][3]['id'] # breaking bad
        print(f"ID is {first_id}")
        
        print(f"Triggering mini modal for {first_id}...")
        js_modal = f"""
        async () => {{
            const response = await fetch(`/mini-modal-info.php?id={first_id}&t={t}`, {{ headers: {{ 'X-Requested-With': 'XMLHttpRequest' }} }});
            return await response.text();
        }}
        """
        await page.evaluate(js_modal)
        
        print(f"Triggering post.php for {first_id}...")
        js_post = f"""
        async () => {{
            const response = await fetch(`/post.php?id={first_id}&t={t}`, {{ headers: {{ 'X-Requested-With': 'XMLHttpRequest' }} }});
            return await response.text();
        }}
        """
        await page.evaluate(js_post)
        
        await page.wait_for_timeout(2000)
        await browser.close()

asyncio.run(main())
