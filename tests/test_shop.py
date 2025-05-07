import pytest
from playwright.sync_api import sync_playwright
from time import time, sleep

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_shop_flow(browser):
    page = browser.new_page()
    page.goto("https://autoprojekt.simplytest.de/")

    # 1. Überschrift prüfen
    assert "Shop" in page.locator("h1").inner_text()

    # 2. Warenkorb prüfen
    cart_count = page.locator(".cart-contents .count").inner_text()
    assert "0" in cart_count.lower()

    # 3. Artikel "Album" direkt aus der Produktübersicht hinzufügen
    page.locator("li.product:has-text('Album') >> text=Add to cart").click()

    # 4. Warten auf Bestätigung
    page.locator("div.woocommerce-message:has-text('Album')").wait_for()

    # 5. "View cart" klicken
    page.locator("a.added_to_cart").click()

    # 6. Warten bis Warenkorb geladen ist
    page.wait_for_url("**/cart/")

    # 7. Menge auf 2 ändern
    qty_input = page.locator("input.qty").first
    qty_input.wait_for(state="visible")
    qty_input.fill("2")

    # 8. Button "Update cart" finden und aktiv auf Aktivierung warten
    update_btn = page.locator("button[name='update_cart']")
    update_btn.wait_for(state="visible")

    start = time()
    timeout = 5  # Sekunden warten auf Aktivierung

    while not update_btn.is_enabled():
        if time() - start > timeout:
            # Screenshot zur Diagnose
            page.screenshot(path="update_cart_disabled.png")
            print("🔍 Diagnose:")
            print("Aktuelle URL:", page.url)
            print("Button enabled:", update_btn.is_enabled())
            print("Button class:", update_btn.get_attribute("class"))
            raise AssertionError("🚫 'Update cart' bleibt deaktiviert, obwohl Menge geändert wurde!")
        sleep(0.2)

    # 9. Klicken
    update_btn.click()

    # 10. Auf Preisanzeige warten
    page.wait_for_timeout(1000)

    # 11. Gesamtpreis prüfen
    total = page.locator("td.product-subtotal > span.woocommerce-Price-amount").inner_text()
    assert "30,00" in total

    print("✅ Test erfolgreich abgeschlossen!")
