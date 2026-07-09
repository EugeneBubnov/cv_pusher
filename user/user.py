from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    phone: str
    telegram: str
    cv_path: str = "cv/cv.pdf"
