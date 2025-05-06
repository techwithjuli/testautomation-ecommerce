import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.closed()

def test_shop_flow(browser):
    page = browser.new_page()

    # 1. Demo Shop öffnen
    page.goto("https://autoprojekt.simplytest.de/")

    # 2. Überschrift prüfen
    heading = page.locator("h1").inner_text()
    assert "Shop" in heading

    # 3. Warenkorb prüfen (leer)
    cart_count = page.locator(".cart-contents .count").inner_text()
    assert cart_count == "0"

    # 4. Artikel "Album" in den Warenkorb legen
    page.locator("text=Album").click()
    page.locator("text=Add to cart").click()

    # 5. Zum Warenkorb gehen
    page.locator("text=View cart").click()

    # 6. Anzahl auf 2 ändern
    qty_input = page.locator("input.qty")
    qty_input.fill("2")

    # 7. Warenkorb aktualisieren
    page.locator("input[name='update_cart']").click()
    page.wait_for_timeout(1000)

    # 8. Gesamtpreis prüfen
    total = page.locator("td.product-subtotal > span.woocommerce-Price-amount").inner_text()
    assert "30,00" in total

    print("✅ Test erfolgreich abgeschlossen!")