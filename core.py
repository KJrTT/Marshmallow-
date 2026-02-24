"""
Модуль core.py - Ядро системы
Содержит модели данных и схемы Marshmallow для демонстрации
"""

from datetime import datetime
from marshmallow import Schema, validate, post_load, pre_dump, post_dump, fields


# ===================== МОДЕЛИ ДАННЫХ =====================

class User:
    """Модель пользователя блога"""

    def __init__(self, id, username, email, registered_on=None, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.registered_on = registered_on or datetime.now()
        self.is_active = is_active

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"


class Article:
    """Модель статьи блога"""

    def __init__(self, id, title, content, author, created_at=None, tags=None, views=0):
        self.id = id
        self.title = title
        self.content = content
        self.author = author  # User object
        self.created_at = created_at or datetime.now()
        self.tags = tags or []
        self.views = views

    def __repr__(self):
        return f"Article(id={self.id}, title='{self.title}')"


class Comment:
    """Модель комментария к статье"""

    def __init__(self, id, text, author, article, created_at=None):
        self.id = id
        self.text = text
        self.author = author  # User object
        self.article = article  # Article object
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"Comment(id={self.id}, author='{self.author.username}')"


# ===================== СХЕМЫ MARSHMALLOW =====================

class UserSchema(Schema):
    """Схема для сериализации/валидации пользователя"""
    id = fields.Int(dump_only=True)  # Только для вывода
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=20),
        error_messages={
            "required": "Имя пользователя обязательно",
            "validator_failed": "Имя пользователя должно быть от 3 до 20 символов"
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email обязателен",
            "invalid": "Некорректный email адрес"
        }
    )
    registered_on = fields.DateTime(dump_only=True)
    is_active = fields.Bool()

    @post_load
    def make_user(self, data, **kwargs):
        """Создание объекта User после загрузки данных"""
        # Временный id = None, потом будет присвоен
        return User(id=None, username=data['username'], email=data['email'])

    @post_dump
    def add_metadata(self, data, **kwargs):
        """Добавление метаданных после сериализации"""
        data['_type'] = 'user'
        return data


class ArticleSchema(Schema):
    """Схема для сериализации/валидации статьи"""
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200),
        error_messages={
            "required": "Заголовок обязателен",
            "validator_failed": "Заголовок должен быть от 5 до 200 символов"
        }
    )
    content = fields.Str(
        required=True,
        error_messages={"required": "Содержание статьи обязательно"}
    )
    author = fields.Nested(lambda: UserSchema())  # Вложенная схема пользователя
    created_at = fields.DateTime(dump_only=True)
    tags = fields.List(fields.Str())
    views = fields.Int(dump_only=True)

    class Meta:
        ordered = True  # Сохранять порядок полей

    @pre_dump
    def prepare_author(self, data, **kwargs):
        """Подготовка данных перед сериализацией"""
        return data

    @post_dump
    def add_preview(self, data, **kwargs):
        """Добавление превью к статье"""
        if 'content' in data and len(data['content']) > 100:
            data['preview'] = data['content'][:100] + '...'
        return data


class CommentSchema(Schema):
    """Схема для сериализации/валидации комментария"""
    id = fields.Int(dump_only=True)
    text = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=500),
        error_messages={
            "required": "Текст комментария обязателен",
            "validator_failed": "Комментарий должен быть от 1 до 500 символов"
        }
    )
    author = fields.Nested(lambda: UserSchema(only=('id', 'username')))  # Только id и username
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_comment(self, data, **kwargs):
        """Создание объекта Comment после загрузки"""
        # Для демо создаем комментарий без article
        return Comment(id=None, text=data['text'], author=data.get('author'), article=None)


# ===================== ТЕСТОВЫЕ ДАННЫЕ =====================

def create_test_data():
    """Создание тестовых данных для демонстраций"""
    # Создаем пользователей
    user1 = User(1, "ivan_petrov", "ivan@example.com", datetime(2024, 1, 15, 10, 30))
    user2 = User(2, "maria_sidorova", "maria@example.com", datetime(2024, 2, 20, 15, 45))

    # Создаем статьи
    article1 = Article(
        1,
        "Введение в Marshmallow",
        "Marshmallow — это библиотека для сериализации и валидации данных в Python. Она позволяет преобразовывать сложные объекты в простые типы данных и обратно.",
        user1,
        datetime(2024, 2, 1, 12, 0),
        ["python", "marshmallow", "tutorial"],
        156
    )

    article2 = Article(
        2,
        "10 советов по валидации данных",
        "Валидация данных — критически важная часть любого приложения. В этой статье мы рассмотрим лучшие практики использования Marshmallow для валидации.",
        user1,
        datetime(2024, 2, 10, 9, 15),
        ["validation", "best-practices"],
        89
    )

    # Создаем комментарии
    comment1 = Comment(1, "Отличная статья, помогла разобраться!", user2, article1)
    comment2 = Comment(2, "Жду продолжения!", user2, article1)
    comment3 = Comment(3, "Спасибо за полезные советы", user1, article2)

    # Добавляем комментарии к статьям (для удобства)
    article1.comments = [comment1, comment2]
    article2.comments = [comment3]

    return {
        'users': [user1, user2],
        'articles': [article1, article2],
        'comments': [comment1, comment2, comment3]
    }
