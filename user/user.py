import json
from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    phone: str
    telegram: str
    comment: str
    cv_path: str = "cv/cv.pdf"

    @classmethod
    def create_user_by_json(cls):
        """Создать пользователя по данным файла user_info.json"""
        with open("user/user_info.json", "r", encoding="utf-8") as file:
            data: dict = json.load(file)

        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            telegram=data["telegram"],
            comment=data["comment"],
        )
