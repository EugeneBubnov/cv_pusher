import logging
from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Locator, Page

logging.basicConfig(
    level=logging.INFO,
    datefmt="[%d.%m.%Y | %H:%M:%S",
    format="%(asctime)s | %(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


@dataclass
class BasePage:
    page: Page
    base_url: str
    page_url: str
    path_params: Optional[str] = None

    @property
    def logger(self):
        return logging.getLogger(self.__class__.__name__)

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
