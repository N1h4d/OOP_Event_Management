# src/utils/validators.py

import re
from datetime import datetime


def normalize_name(name: str) -> str:
    """
    Adı trim edir, ilk hərfi böyük, qalan hamısını kiçik edir.
    Boş ola bilməz.
    """
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    return name[0].upper() + name[1:].lower()


def normalize_full_name(full_name: str) -> str:
    """
    Full name üçün: artıq boşluqları kəsir,
    hər sözü ilk hərfi böyük, qalanı kiçik edir.
    """
    full_name = full_name.strip()
    if not full_name:
        raise ValueError("Full name cannot be empty.")

    parts = [p for p in full_name.split(" ") if p]
    return " ".join(p.capitalize() for p in parts)


def validate_positive_int(raw: str, field_name: str) -> int:
    """
    Müsbət tam ədəd olmalıdır (> 0).
    Məs: Capacity, Age, Duration.
    """
    raw = raw.strip()
    if not raw:
        raise ValueError(f"{field_name} is required.")

    if not re.fullmatch(r"-?\d+", raw):
        raise ValueError(f"{field_name} must be an integer number.")

    value = int(raw)
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")
    return value


def validate_price(raw: str) -> float:
    """
    Price üçün: 0-dan böyük real ədəd.
    """
    raw = raw.strip()
    if not raw:
        raise ValueError("Price is required.")

    try:
        value = float(raw)
    except ValueError:
        raise ValueError("Price must be a number.")

    if value < 0:
        raise ValueError("Price cannot be negative.")
    return value


def validate_phone(phone: str) -> str:
    """
    Telefon: yalnız rəqəmlər, 10 rəqəm.
    Məs: 0501234567, 0519876543
    """
    phone = phone.strip()
    if not phone:
        raise ValueError("Phone is required.")

    if not re.fullmatch(r"\d{10}", phone):
        raise ValueError("Phone must contain exactly 10 digits (e.g. 0501234567).")

    return phone


def validate_email(email: str) -> str:
    """
    Sadə email yoxlaması.
    """
    email = email.strip()
    if not email:
        raise ValueError("Email is required.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Email format is invalid (e.g. user@example.com).")

    return email


def validate_gender(gender: str) -> str:
    """
    Gender: yalnız M və ya F (case-insensitive).
    """
    g = gender.strip().upper()
    if g not in ("M", "F"):
        raise ValueError("Gender must be 'M' or 'F'.")
    return g


def validate_date(date_str: str) -> str:
    """
    Tarix formatı: YYYY-MM-DD, məs: 2025-06-01
    """
    date_str = date_str.strip()
    if not date_str:
        raise ValueError("Date is required.")

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in format YYYY-MM-DD (e.g. 2025-06-01).")

    # eyni formatda geri qaytarırıq
    return dt.strftime("%Y-%m-%d")


def validate_time(time_str: str) -> str:
    """
    Saat formatı: HH:MM (24 saat)
    """
    time_str = time_str.strip()
    if not time_str:
        raise ValueError("Time is required.")

    try:
        t = datetime.strptime(time_str, "%H:%M")
    except ValueError:
        raise ValueError("Time must be in format HH:MM (e.g. 09:30).")

    return t.strftime("%H:%M")


def validate_yes_no(choice: str, field_name: str) -> bool:
    """
    'y' / 'n' inputunu bool-a çevirir.
    """
    c = choice.strip().lower()
    if c not in ("y", "n"):
        raise ValueError(f"{field_name} must be 'y' or 'n'.")
    return c == "y"
