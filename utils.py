"""
Модуль utils.py - Вспомогательные функции и кастомные поля
"""

import json
from marshmallow import fields, ValidationError
from functools import wraps
import time
from datetime import datetime


# ===================== ФОРМАТИРОВАНИЕ ВЫВОДА =====================

def pretty_print(data, title=None):
    """
    Красивый вывод данных в формате JSON

    Args:
        data: Данные для вывода (dict, list или объект)
        title: Заголовок для вывода
    """
    if title:
        print(f"\n--- {title} ---")

    # Преобразуем в JSON с отступами
    try:
        if hasattr(data, '__dict__') and not isinstance(data, (dict, list)):
            # Если это объект с __dict__, но не словарь и не список
            data = {k: v for k, v in data.__dict__.items() if not k.startswith('_')}

        # Специальная обработка для datetime и других несериализуемых типов
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if hasattr(obj, '__dict__'):
                return str(obj)
            return str(obj)

        print(json.dumps(data, indent=2, default=json_serializer, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка форматирования: {e}")
        print(data)


def print_separator(char="=", length=60):
    """Печать разделителя"""
    print(char * length)


def print_header(text):
    """Печать заголовка"""
    print_separator()
    print(f" {text}")
    print_separator()


# ===================== КАСТОМНЫЕ ПОЛЯ MARSHMALLOW =====================

class PasswordField(fields.Field):
    """
    Кастомное поле для валидации пароля

    Требования:
    - Минимум 8 символов
    - Хотя бы одна цифра
    - Хотя бы одна буква в верхнем регистре
    - Хотя бы одна буква в нижнем регистре
    """

    def _deserialize(self, value, attr, data, **kwargs):
        """Валидация и десериализация значения"""
        if not isinstance(value, str):
            raise ValidationError("Пароль должен быть строкой")

        errors = []

        # Проверка длины
        if len(value) < 8:
            errors.append("минимум 8 символов")

        # Проверка наличия цифр
        if not any(c.isdigit() for c in value):
            errors.append("хотя бы одну цифру")

        # Проверка наличия букв в верхнем регистре
        if not any(c.isupper() for c in value):
            errors.append("хотя бы одну заглавную букву")

        # Проверка наличия букв в нижнем регистре
        if not any(c.islower() for c in value):
            errors.append("хотя бы одну строчную букву")

        if errors:
            raise ValidationError(f"Пароль должен содержать: {', '.join(errors)}")

        return value  # В реальном проекте здесь должен быть хэш пароля


class PhoneField(fields.Field):
    """
    Кастомное поле для валидации российских телефонных номеров

    Поддерживаемые форматы:
    - +7XXXXXXXXXX
    - 8XXXXXXXXXX
    - +7 (XXX) XXX-XX-XX
    """

    def _deserialize(self, value, attr, data, **kwargs):
        """Валидация и десериализация телефонного номера"""
        if not isinstance(value, str):
            raise ValidationError("Телефон должен быть строкой")

        # Очищаем номер от лишних символов
        cleaned = ''.join(c for c in value if c.isdigit() or c == '+')

        # Проверяем длину
        if len(cleaned) == 11 and cleaned.startswith('8'):
            # 8XXXXXXXXXX -> +7XXXXXXXXXX
            cleaned = '+7' + cleaned[1:]
        elif len(cleaned) == 12 and cleaned.startswith('+7'):
            pass  # Уже правильный формат
        else:
            raise ValidationError("Некорректный формат номера. Используйте +7XXXXXXXXXX или 8XXXXXXXXXX")

        # Проверяем, что после +7 идут только цифры
        if not cleaned[2:].isdigit():
            raise ValidationError("Номер должен содержать только цифры после кода страны")

        return cleaned


# ===================== ДЕКОРАТОРЫ =====================

def timer(func):
    """
    Декоратор для замера времени выполнения функции
    Использует @wraps для сохранения метаданных
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"\n⏱️  Время выполнения '{func.__name__}': {elapsed:.6f} секунд")
        return result

    return wrapper


# ===================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====================

def validate_password_strength(password):
    """
    Функция для проверки сложности пароля (для демонстрации)

    Returns:
        tuple: (is_valid, errors)
    """
    field = PasswordField()
    try:
        field.deserialize(password)
        return True, []
    except ValidationError as e:
        return False, e.messages if isinstance(e.messages, list) else [str(e.messages)]


def create_sample_registration_data():
    """Создание тестовых данных для регистрации"""
    return [
        # Корректные данные
        {
            "username": "newuser",
            "email": "user@example.com"
        },
        # Некорректный email
        {
            "username": "testuser",
            "email": "not-an-email"
        },
        # Короткое имя
        {
            "username": "a",
            "email": "a@example.com"
        }
    ]
