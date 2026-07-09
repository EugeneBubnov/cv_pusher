from urllib.parse import urlencode

from pages.ozon_tech.ozon_vacancy_page import OzonVacancyPage
from user.user import User
from utils.browser_manager import browser_session


def main(user: User):
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


if __name__ == "__main__":
    user = User.create_user_by_hh_cv()

    main(user)
