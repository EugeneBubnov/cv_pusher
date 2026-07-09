from dataclasses import dataclass

from utils.pdf_parser import parse_pdf_text


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    phone: str
    telegram: str
    cv_path: str = "cv/cv.pdf"

    @classmethod
    def create_user_by_hh_cv(cls):
        """Создать пользователя по данным из резюме с hh.ru"""
        user_cv_data: dict = {}

        cv_info = parse_pdf_text(cls.cv_path).split("\n")
        user_cv_data["first_name"] = cv_info[0].split(" ")[1]
        user_cv_data["last_name"] = cv_info[0].split(" ")[0]
        user_cv_data["email"] = (
            cv_info[3]
            .split(" ")[0]
            .replace(" — предпочитаемый способ связи", "")
            .strip()
        )
        user_cv_data["phone"] = (
            cv_info[2]
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
            .replace("+7", "")
            .strip()
        )
        user_cv_data["telegram"] = cv_info[5].split(" ")[1].strip()

        return cls(
            first_name=user_cv_data.get("first_name"),
            last_name=user_cv_data.get("last_name"),
            email=user_cv_data.get("email"),
            phone=user_cv_data.get("phone"),
            telegram=user_cv_data.get("telegram"),
        )
