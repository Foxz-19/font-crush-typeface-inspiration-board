import json
import time
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright, Error

class TestServer(ThreadingHTTPServer):
    allow_reuse_address = False

server = TestServer(("127.0.0.1", 8765), SimpleHTTPRequestHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    for attempt in range(3):
        try:
            page.goto("http://127.0.0.1:8765", wait_until="domcontentloaded")
            break
        except Error:
            if attempt == 2:
                raise
            time.sleep(.2)
    page.fill("#font-name", "Lora")
    page.select_option("#category", "serif")
    page.select_option("#mood", "cozy")
    page.fill("#spotted", "Book cover")
    page.fill("#sample", "Letters worth keeping.")
    page.click("button[type=submit]")
    page.wait_for_selector(".specimen")
    assert page.locator(".specimen h3").inner_text() == "Lora"
    page.reload(wait_until="domcontentloaded")
    assert page.locator(".specimen").count() == 1
    page.click(".edit")
    assert page.locator("#submit-label").inner_text() == "Save changes"
    page.fill("#spotted", "Editorial cover")
    page.click("button[type=submit]")
    assert "Editorial cover" in page.locator(".spotted").inner_text()
    page.select_option("#mood-filter", "bold")
    assert page.locator(".specimen").count() == 0
    page.click("#clear-filters")
    page.click(".delete")
    assert "Lora" in page.locator("#delete-copy").inner_text()
    page.click(".danger")
    page.wait_for_selector(".specimen", state="detached")
    page.click("#undo-delete")
    page.wait_for_selector(".specimen")
    assert page.locator(".specimen").count() == 1
    page.click(".delete")
    page.click(".danger")
    page.wait_for_selector(".specimen", state="detached")
    page.set_input_files("#import-file", {"name": "bad.json", "mimeType": "application/json", "buffer": b"{}"})
    assert "Nothing was imported" in page.locator("#notice").inner_text()
    backup = [{"id": "import-1", "fontName": "Lora", "category": "serif", "spotted": "Imported book", "sample": "Portable type.", "mood": "elegant", "dateSaved": "2026-01-01T00:00:00.000Z"}]
    page.set_input_files("#import-file", {"name": "fonts.json", "mimeType": "application/json", "buffer": json.dumps(backup).encode()})
    page.wait_for_selector(".specimen")
    with page.expect_download() as download:
        page.click("#export-data")
    assert download.value.suggested_filename.startswith("font-crush-")
    page.set_viewport_size({"width": 375, "height": 812})
    page.click(".mobile-add")
    assert page.locator("#composer").evaluate("el => el.classList.contains('open')")
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.locator("#font-name").get_attribute("aria-describedby") == "font-name-error"
    page.keyboard.press("Escape")
    assert not page.locator("#composer").evaluate("el => el.classList.contains('open')")
    assert not errors, errors
    browser.close()
    server.shutdown()
    server.server_close()
    print("E2E PASS: create/edit, persist, filter, delete/undo, import/export, mobile/a11y, no page errors")
