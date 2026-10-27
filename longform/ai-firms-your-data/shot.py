"""Screenshot an HTML page with Playwright: python3 shot.py PAGE.html OUT.png WIDTH HEIGHT"""
import sys, asyncio
from playwright.async_api import async_playwright
async def main(html, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.goto("file://" + __import__("os").path.abspath(html)); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=out); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
