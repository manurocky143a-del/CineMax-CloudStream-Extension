import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False) # Headful so Cloudflare Turnstile might auto-pass or solve
        page = await browser.new_page()

        requests_log = []

        async def handle_request(req):
            requests_log.append({
                "method": req.method,
                "url": req.url,
                "headers": dict(req.headers),
                "resource_type": req.resource_type
            })

        async def handle_response(res):
            if res.request.resource_type in ["xhr", "fetch", "document"]:
                try:
                    text = await res.text()
                    print(f"RESPONSE [{res.status}] {res.url} ({len(text)} bytes):")
                    print(text[:300])
                    print("-" * 40)
                except Exception as e:
                    pass

        page.on("request", handle_request)
        page.on("response", handle_response)

        print("Navigating to net77.cc/home...")
        try:
            await page.goto("https://net77.cc/home", timeout=30000)
        except Exception as e:
            print("Goto info:", e)

        # Give it 15 seconds for Cloudflare Turnstile to solve
        print("Waiting 15 seconds...")
        await page.wait_for_timeout(15000)

        title = await page.title()
        print("FINAL PAGE TITLE:", title)

        # Save HTML
        html = await page.content()
        with open("net77_browser_rendered.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Save cookies
        cookies = await page.context.cookies()
        print("COOKIES:")
        for c in cookies:
            print(f"  {c['name']} = {c['value']} (domain={c['domain']})")

        await browser.close()

asyncio.run(main())
