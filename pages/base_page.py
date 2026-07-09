from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Locator, Page


@dataclass
class BasePage:
    page: Page
    base_url: str
    page_url: str
    path_params: Optional[str] = None

    def open_page(self) -> None:
        """Открыть текущую страницу"""
        if self.path_params:
            self.page.goto(f"{self.base_url}/{self.page_url}/{self.path_params}")
        else:
            self.page.goto(f"{self.base_url}/{self.page_url}")

        self.page.wait_for_load_state("domcontentloaded")

    def find(self, locator: str) -> Locator:
        """Найти локатор"""
        return self.page.locator(locator)
