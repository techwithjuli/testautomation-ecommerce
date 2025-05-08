import asyncio
from playwright.async_api import async_playwright

URL = "https://autoprojekt.simplytest.de/"

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=True für unsichtbare Tests
        page = await browser.new_page()

        # 1. Shop öffnen
        await page.goto(URL)

        # 2. Überschrift prüfen
        heading = await page.locator("h1").inner_text()
        assert "Shop" in heading, f"Erwartet: 'Shop' in '{heading}'"

        # 3. Warenkorb prüfen (leer)
        cart_count = await page.locator(".cart-contents .count").inner_text()
        assert "0" in cart_count.lower(), f"Warenkorb ist nicht leer: {cart_count}"

        # 4. Artikel "Album" hinzufügen
        await page.locator("li.product:has-text('Album') >> text=Add to cart").click()

        # 5. Zum Warenkorb wechseln
        await page.locator("a.added_to_cart").click()
        page.wait_for_timeout(500)

        # 6. Anzahl auf 2 erhöhen
        qty_input = page.locator("input.qty").first
        qty_input.wait_for(state="visible")

        #qty_input.fill("1")
        #qty_input.press("Enter")
        #page.wait_for_timeout(500)

        qty_input.fill("2")
        qty_input.press("Enter")
        page.wait_for_timeout(500)

        # 7. "Update cart" klicken
        await page.locator("input[name='update_cart'] >> [type=submit]").click()

        # 8. Gesamtpreis überprüfen
        await page.wait_for_timeout(1000)  # kleine Wartezeit für Aktualisierung
        total = await page.locator("td.product-subtotal > span.woocommerce-Price-amount").inner_text()
        assert "30,00" in total, f"Erwarteter Preis 30,00 €, gefunden: {total}"

        print("✅ Test erfolgreich abgeschlossen!")

        await browser.close()

asyncio.run(run_test())
