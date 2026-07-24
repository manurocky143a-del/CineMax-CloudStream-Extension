import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        media_requests = []

        async def handle_request(req):
            url = req.url
            if ".m3u8" in url or ".ts" in url or "play.php" in url or "playlist.php" in url or "nm-cdn" in url or "files" in url:
                print(f"REQUEST [{req.method}]: {url}")
                print(f"  Headers: {dict(req.headers)}")
                media_requests.append({
                    "method": req.method,
                    "url": url,
                    "headers": dict(req.headers)
                })

        async def handle_response(res):
            url = res.url
            if ".m3u8" in url or ".ts" in url or "play.php" in url or "playlist.php" in url:
                try:
                    body = await res.text()
                    print(f"RESPONSE [{res.status}]: {url}")
                    print(f"  Body (first 300 chars): {body[:300]}")
                    print("-" * 50)
                except Exception as e:
                    pass

        page.on("request", handle_request)
        page.on("response", handle_response)

        print("Navigating to https://net77.cc/ ...")
        await page.goto("https://net77.cc/", wait_until="domcontentloaded")
        await page.wait_for_timeout(10000)

        # Trigger search for Batman Begins (70021642)
        print("Searching for Batman...")
        await page.evaluate("""
        async () => {
            const t = Math.floor(Date.now() / 1000);
            const res = await fetch('/search.php?s=batman&t=' + t, {headers: {'X-Requested-With': 'XMLHttpRequest'}});
            const data = await res.json();
            console.log('Search:', data);
        }
        """)
        await page.wait_for_timeout(2000)

        # Trigger play.php
        print("Triggering play.php...")
        token_h = await page.evaluate("""
        async () => {
            const res = await fetch('/play.php', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                },
                body: 'id=70021642'
            });
            const data = await res.json();
            return data.h;
        }
        """)
        print("Token h from play.php:", token_h)

        # Trigger playlist.php
        print("Triggering playlist.php...")
        playlist_json = await page.evaluate("""
        async () => {
            const t = Math.floor(Date.now() / 1000);
            const res = await fetch('/playlist.php?id=70021642&t=Batman%20Begins&tm=' + t, {
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            });
            return await res.json();
        }
        """)
        print("Playlist JSON from browser:", playlist_json)

        # Fetch master m3u8 from inside browser context with token
        if token_h:
            hls_path = playlist_json[0]["sources"][0]["file"].replace("in=unknown::ni", token_h)
            print("Fetching HLS path inside browser:", hls_path)
            master_m3u8 = await page.evaluate(f"""
            async () => {{
                const res = await fetch('{hls_path}');
                return await res.text();
            }}
            """)
            print("Master M3U8 from browser context:\n", master_m3u8[:500])

        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(main())
