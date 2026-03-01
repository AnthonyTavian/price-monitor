from playwright.async_api import async_playwright

async def scrape_amazon_price(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        await page.goto(url, wait_until="domcontentloaded")

        
        try:
            price_whole = await page.locator(".a-price-whole").first.inner_text()
            price_fraction = await page.locator(".a-price-fraction").first.inner_text()
            price_whole = price_whole.replace('.', '').replace(',', '').replace('\n', '').strip()
            price_fraction = price_fraction.replace('\n', '').strip()
            price = float(f"{price_whole}.{price_fraction}")
        except:
            raise ValueError("Price not found on page")
        
        try:
            name = await page.locator("#productTitle").inner_text()
            name = name.strip()
        except:
            name = "Unknown"
        
        await browser.close()
        
        return {
            "price": price,
            "name": name
        }