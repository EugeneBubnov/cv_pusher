import json
import logging
from urllib.parse import urlencode

from playwright.sync_api import Response, expect

from pages.base_page import BasePage
from pages.ozon_tech.ozon_vacancy_locators import OzonVacancyLocators as l
from user.user import User
from utils.browser_manager import browser_session

logging.basicConfig(
    level=logging.INFO,
    datefmt="[%d.%m.%Y | %H:%M:%S",
    format="%(asctime)s | %(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
    ],
)

logger = logging.getLogger(__name__)


class OzonVacancyPage(BasePage):
    def get_current_vacancy_list(self) -> list:
        """Получить ссылки на страницы вакансий

        Returns:
            list: список url с вакансиями
        """
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.find(l.CURRENT_VACANCY_LIST).last).to_be_visible(timeout=10_000)

        vacancy_list = self.find(l.CURRENT_VACANCY_LIST).all()
        links = []

        for vacancy in vacancy_list:
            link = vacancy.get_attribute(name="href", timeout=5000)
            links.append(link)
            logger.info(f"Найдена ссылка: {self.base_url}{link}")

        return links

    def open_card_by_link(self, link: str):
        """Открыть карточку вакансии по ссылке

        Args:
            link (str): ссылка на вакансию
        """
        self.page.goto(f"{self.base_url}{link}")
        self.page.wait_for_load_state("networkidle")
        logger.info(f"Выполнен переход по ссылке: {self.base_url}{link}")

    def read_vacancy(self):
        """Прочитать вакансию"""
        expect(self.find(l.CARD_HEADING)).to_be_visible(timeout=10_000)

        vacancy_info: dict = {}
        # Название
        vacancy_info["name"] = self.find(l.CARD_HEADING).text_content()

        # Требования
        requirements_locators = self.find(l.REQ_LIST).all()
        requirements = []

        for req in requirements_locators:
            requirements.append(req.text_content())

        vacancy_info["requirements"] = requirements

        logger.info(
            f"Найдены данные по вакансии:\n{json.dumps(vacancy_info, indent=2, ensure_ascii=False)}"
        )

    def click_on_submit_button(self):
        """Нажать кнопку: [Откликнуться]"""
        self.find(l.OPEN_MODAL_BTN).click()

    def complete_the_form(self, user: User):
        """Заполнить форму данными пользователя

        Args:
            user (User): Пользователь
        """
        for attr_name, attr_value in user.__dict__.items():
            if attr_value is None or attr_value == "":
                error_msg = (
                    f"Атрибут '{attr_name}' не может быть пустым, "
                    f"текущее значение: '{attr_value}'"
                )
                logger.error(error_msg)
                raise AttributeError(error_msg)

        logger.info(
            f"Форма будет заполнена данными пользователя: {json.dumps(user.__dict__, indent=2, ensure_ascii=False)}"
        )

        expect(self.find(l.MODAL_HEADING)).to_be_visible(timeout=10_000)
        self.find(l.LAST_NAME).fill(user.last_name)
        self.find(l.FIRST_NAME).fill(user.first_name)
        self.find(l.EMAIL).fill(user.email)
        self.find(l.PHONE).fill(user.phone)
        self.find(l.TG).fill(user.telegram)
        self.find(l.FILE_BTN).click()

        self.page.wait_for_timeout(1000)
        self.find(l.FILE_INPUT).set_input_files(user.cv_path)

        checkboxes = self.find(l.CHECK_BOX_LIST).all()
        for checkbox in checkboxes:
            checkbox.click()

        with self.page.expect_response(
            "https://ozon.tech/p-api/ozon-tech/vacancy/apply"
        ) as response_info:
            self.page.pause()
            self.find(l.SUBMIT_BTN).click()

        response: Response = response_info.value
        assert response.status == 200, (
            f"Не удалось отправить резюме, статус код ответа: {response.status}"
        )

        self.page.wait_for_timeout(1000)
        logger.info("Резюме отправлено успешно")

    @staticmethod
    def push_cv(user: User):
        """Выполняет процесс отправки резюме"""
        with browser_session() as page:
            # Ввести параметры поиска вакансии
            query_params = {
                "search": "авто",
                "directions": "Тестирование",
                "levels": "Middle",
                "techs": "Python",
                "work_formats": "Удалённая работа",
            }

            path_params = f"?{urlencode(query_params)}"

            ozon_page = OzonVacancyPage(
                page=page,
                base_url="https://ozon.tech",
                page_url="vacancies",
                path_params=path_params,
            )

            ozon_page.open_page()
            links = ozon_page.get_current_vacancy_list()

            for link in links:
                ozon_page.open_card_by_link(link)
                ozon_page.read_vacancy()
                ozon_page.click_on_submit_button()
                ozon_page.complete_the_form(user)
