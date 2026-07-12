from pages.ozon_tech.ozon_vacancy_page import OzonVacancyPage
from user.user import User


def main():
    user = User.create_user_by_json()
    company_pages = [OzonVacancyPage]

    for page in company_pages:
        page.push_cv(user)


if __name__ == "__main__":
    main()
