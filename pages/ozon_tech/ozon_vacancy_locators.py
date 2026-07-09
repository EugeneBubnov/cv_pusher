class OzonVacancyLocators:
    # Общий список вакансий
    CURRENT_VACANCY_LIST = "//div[contains(@class, 'vacanciesWrapper')]/a"

    # Карточка вакансии
    CARD_HEADING = "//h1[contains(@class, 'headline-hero')]"
    REQ_LIST = "//div[contains(@class, 'descriptionHtml')]/ul[2]/li"
    OPEN_MODAL_BTN = "(//button[contains(.,'Откликнуться')])[1]"

    # Модальное окно
    MODAL_HEADING = "//div[.='Отклик на вакансию']"
    LAST_NAME = "//label[contains(.,'Фамилия')]/ancestor::div[1]/div/div/div/input"
    FIRST_NAME = "//label[contains(.,'Имя')]/ancestor::div[1]/div/div/div/input"
    EMAIL = "//label[contains(.,'Email')]/ancestor::div[1]/div/div/div/input"
    TG = "//label[contains(.,'Telegram')]/ancestor::div[1]/div/div/div/input"
    PHONE = "//input[contains(@placeholder,'Телефон')]"
    FILE_BTN = "//div[.='Файл']/div"
    FILE_INPUT = "[type='file']"
    CHECK_BOX_LIST = "[type='checkbox']"
    SUBMIT_BTN = "(//div[.='Отправить'])[3]"
    POP_UP = "//div[.='Отклик отправлен']"
