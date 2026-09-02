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
    edited_spot = page.locator(".spotted").text_content()
    assert "Editorial cover" in edited_spot, edited_spot
    page.select_option("#mood-filter", "bold")
    assert page.locator(".specimen").count() == 0
    assert "mood=bold" in page.url
    page.click("#clear-filters")
    assert "mood=" not in page.url
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
    attack = [{"id": '\"><img src=x onerror=alert(1)>', "fontName": "Lora", "category": "serif", "spotted": "Attack", "sample": "Unsafe", "mood": "bold", "dateSaved": "2026-01-01T00:00:00.000Z"}]
    page.set_input_files("#import-file", {"name": "bad.json", "mimeType": "application/json", "buffer": json.dumps(attack).encode()})
    assert "Nothing was imported" in page.locator("#notice").inner_text()
    assert page.locator("img").count() == 0
    backup = [{"id": "import-1", "fontName": "Lora", "category": "serif", "spotted": "Imported book", "sample": "Portable type.", "mood": "elegant", "dateSaved": "2026-01-01T00:00:00.000Z"}]
    page.set_input_files("#import-file", {"name": "fonts.json", "mimeType": "application/json", "buffer": json.dumps(backup).encode()})
    page.wait_for_selector(".specimen")
    with page.expect_download() as download:
        page.click("#export-data")
    assert download.value.suggested_filename.startswith("font-crush-")
    page.set_viewport_size({"width": 375, "height": 812})
    assert page.locator("#composer").get_attribute("inert") is not None
    assert page.locator(".mobile-add").get_attribute("aria-expanded") == "false"
    page.click(".mobile-add")
    assert page.locator("#composer").evaluate("el => el.classList.contains('open')")
    assert page.locator("#composer").get_attribute("inert") is None
    assert page.locator(".mobile-add").get_attribute("aria-expanded") == "true"
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.locator("#font-name").get_attribute("aria-describedby") == "font-name-error"
    page.fill("#font-name", "Unsaved Draft")
    page.keyboard.press("Escape")
    assert page.locator("#draft-dialog").evaluate("el => el.open")
    page.click("#draft-dialog button[value=keep]")
    assert page.locator("#composer").evaluate("el => el.classList.contains('open')")
    page.keyboard.press("Escape")
    page.click("#draft-dialog button[value=discard]")
    assert not page.locator("#composer").evaluate("el => el.classList.contains('open')")
    assert page.locator("#composer").get_attribute("inert") is not None
    page.add_script_tag(url="http://127.0.0.1:8765/node_modules/axe-core/axe.min.js")
    axe = page.evaluate("axe.run()")
    serious = [item for item in axe["violations"] if item["impact"] in ("serious", "critical")]
    assert not serious, [(item["id"], [(node["target"], node["failureSummary"]) for node in item["nodes"]]) for item in serious]
    assert not errors, errors
    browser.close()
    server.shutdown()
    server.server_close()
    print("E2E PASS: create/edit, persist, filter, delete/undo, import/export, mobile/a11y, no page errors")
