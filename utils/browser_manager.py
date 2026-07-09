# core/browser_manager.py
from contextlib import contextmanager

from playwright.sync_api import sync_playwright


@contextmanager
def browser_session(headless: bool = False):
    """Контекстный менеджер для браузера"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        try:
            yield page
        finally:
            page.close()
            context.close()
            browser.close()
