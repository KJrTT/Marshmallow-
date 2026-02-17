"""
Модуль logic.py - Логика демонстраций Marshmallow
"""

from core import (
    User, Article, Comment,
    UserSchema, ArticleSchema, CommentSchema,
    create_test_data
)
from utils import (
    pretty_print, print_header, timer,
    PasswordField, PhoneField,
    create_sample_registration_data,
    validate_password_strength
)
from marshmallow import ValidationError, fields, pre_dump, post_dump
from datetime import datetime


# ===================== ДЕМОНСТРАЦИЯ 1: БАЗОВАЯ СЕРИАЛИЗАЦИЯ =====================

@timer
def demo_basic_serialization():
    """
    Демонстрация базовой сериализации объектов в JSON
    """
    print_header("📄 ДЕМО 1: БАЗОВАЯ СЕРИАЛИЗАЦИЯ (ОБЪЕКТ → JSON)")

    # Получаем тестовые данные
    data = create_test_data()
    user = data['users'][0]

    print("\n🔹 Исходный объект:")
    print(f"   {user}")

    # Сериализация одного объекта
    print("\n🔹 Сериализация одного пользователя:")
    user_schema = UserSchema()
    result = user_schema.dump(user)
    pretty_print(result, "UserSchema.dump(user)")

    # Демонстрация dump_only полей
    print("\n🔹 Демонстрация dump_only (поля только для вывода):")
    print("   - id: только для вывода (не принимается от клиента)")
    print("   - registered_on: только для вывода (устанавливается сервером)")

    # Сериализация списка объектов
    print("\n🔹 Сериализация списка пользователей (many=True):")
    users = data['users']
    result_list = user_schema.dump(users, many=True)
    pretty_print(result_list, f"Список из {len(users)} пользователей")

    # Сериализация статьи с автором
    print("\n🔹 Сериализация статьи с автором:")
    article = data['articles'][0]
    article_schema = ArticleSchema()
    article_result = article_schema.dump(article)
    pretty_print(article_result, "Article с вложенным автором")

    print("\n✅ Демонстрация базовой сериализации завершена")


# ===================== ДЕМОНСТРАЦИЯ 2: ВАЛИДАЦИЯ ДАННЫХ =====================

@timer
def demo_validation():
    """
    Демонстрация валидации входящих данных
    """
    print_header("✅ ДЕМО 2: ВАЛИДАЦИЯ ДАННЫХ (JSON → ОБЪЕКТ)")

    # Создаем схему
    user_schema = UserSchema()

    # Тестовые данные для регистрации
    test_cases = create_sample_registration_data()

    for i, test_data in enumerate(test_cases, 1):
        print(f"\n🔹 Тест {i}: {test_data}")

        try:
            # Пытаемся валидировать и загрузить данные
            result = user_schema.load(test_data)
            print(f"   ✓ Успех! Валидированные данные:")
            print(f"     {result}")
        except ValidationError as err:
            print(f"   ✗ Ошибки валидации:")
            for field, messages in err.messages.items():
                if isinstance(messages, list):
                    print(f"     - {field}: {', '.join(messages)}")
                else:
                    print(f"     - {field}: {messages}")

    # Демонстрация работы валидаторов
    print("\n🔹 Демонстрация работы валидаторов:")
    print("   - EmailField: автоматическая проверка формата email")
    print("   - Length: проверка длины строки")
    print("   - Required: проверка обязательных полей")

    print("\n✅ Демонстрация валидации завершена")


# ===================== ДЕМОНСТРАЦИЯ 3: ВЛОЖЕННЫЕ СТРУКТУРЫ =====================

@timer
def demo_nested_structures():
    """
    Демонстрация работы с вложенными объектами
    """
    print_header("🔗 ДЕМО 3: ВЛОЖЕННЫЕ СТРУКТУРЫ")

    data = create_test_data()
    article = data['articles'][0]

    print("\n🔹 Полная структура статьи с автором и комментариями:")

    # Создаем схему с полной структурой
    class FullArticleSchema(ArticleSchema):
        comments = fields.Nested(
            lambda: CommentSchema,
            many=True,
            only=('id', 'text', 'author', 'created_at')
        )

    # Временно добавляем комментарии к статье
    article.comments = [c for c in data['comments'] if c.article.id == article.id]

    full_schema = FullArticleSchema()
    result = full_schema.dump(article)
    pretty_print(result, "Статья с комментариями")

    # Демонстрация выборки полей
    print("\n🔹 Выборка только определенных полей (only parameter):")
    minimal_schema = ArticleSchema(only=('id', 'title', 'author.username'))
    minimal_result = minimal_schema.dump(article)
    pretty_print(minimal_result, "Только id, title и author.username")

    # Демонстрация исключения полей
    print("\n🔹 Исключение полей (exclude parameter):")
    no_content_schema = ArticleSchema(exclude=('content',))
    no_content_result = no_content_schema.dump(article)
    pretty_print(no_content_result, "Статья без content")

    print("\n✅ Демонстрация вложенных структур завершена")


# ===================== ДЕМОНСТРАЦИЯ 4: КАСТОМНЫЕ ПОЛЯ И ХУКИ =====================

@timer
def demo_custom_fields():
    """
    Демонстрация кастомных полей и хуков
    """
    print_header("⚙️ ДЕМО 4: КАСТОМНЫЕ ПОЛЯ И ХУКИ")

    # Демонстрация кастомного поля PasswordField
    print("\n🔹 Кастомное поле PasswordField:")

    test_passwords = [
        "12345",
        "password",
        "Password",
        "Pass123",
        "StrongP@ssw0rd"
    ]

    for pwd in test_passwords:
        is_valid, errors = validate_password_strength(pwd)
        if is_valid:
            print(f"   ✓ '{pwd}' - Пароль принят")
        else:
            print(f"   ✗ '{pwd}' - Ошибки: {', '.join(errors)}")

    # Демонстрация кастомного поля PhoneField
    print("\n🔹 Кастомное поле PhoneField:")
    phone_field = PhoneField()

    test_phones = [
        "+79261234567",
        "89261234567",
        "+7 (926) 123-45-67",
        "12345",
        "+7123"
    ]

    for phone in test_phones:
        try:
            result = phone_field.deserialize(phone)
            print(f"   ✓ '{phone}' -> {result}")
        except ValidationError as e:
            print(f"   ✗ '{phone}' - Ошибка: {e.messages}")

    # Демонстрация хуков
    print("\n🔹 Демонстрация хуков:")

    data = create_test_data()
    article = data['articles'][0]

    class DemoHooksSchema(ArticleSchema):
        @pre_dump
        def pre_dump_hook(self, data, **kwargs):
            print(f"   🔧 pre_dump: Модифицируем данные перед сериализацией")
            if hasattr(data, 'views'):
                data.views += 1  # Увеличиваем счетчик просмотров
            return data

        @post_dump
        def post_dump_hook(self, data, **kwargs):
            print(f"   🔧 post_dump: Добавляем метаданные после сериализации")
            data['_processed'] = True
            data['_timestamp'] = str(datetime.now())
            return data

    hook_schema = DemoHooksSchema()
    result = hook_schema.dump(article)
    print(f"   Результат с метаданными:")
    pretty_print(result, "После хуков")

    print("\n✅ Демонстрация кастомных полей и хуков завершена")


# ===================== ДЕМОНСТРАЦИЯ 5: ЧАСТИЧНОЕ ОБНОВЛЕНИЕ =====================

@timer
def demo_partial_update():
    """
    Демонстрация частичного обновления объектов
    """
    print_header("✏️ ДЕМО 5: ЧАСТИЧНОЕ ОБНОВЛЕНИЕ (PARTIAL)")

    # Создаем существующего пользователя
    existing_user = User(1, "old_username", "old@example.com")

    print("\n🔹 Существующий пользователь:")
    print(f"   ID: {existing_user.id}")
    print(f"   Username: {existing_user.username}")
    print(f"   Email: {existing_user.email}")
    print(f"   Зарегистрирован: {existing_user.registered_on}")
    print(f"   Активен: {existing_user.is_active}")

    # Данные для обновления (только некоторые поля)
    update_data = {"username": "new_username"}

    print(f"\n🔹 Данные для обновления: {update_data}")

    # Обычная загрузка (без partial) - потребует все required поля
    print("\n🔹 Без partial (ошибка - email required):")
    try:
        UserSchema().load(update_data)
        print("   Это сообщение не должно появиться")
    except ValidationError as e:
        print(f"   ✗ Ошибка: {e.messages}")

    # Частичное обновление с partial=True
    print("\n🔹 С partial=True (обновляются только указанные поля):")
    try:
        validated_data = UserSchema().load(update_data, partial=True)
        print(f"   ✓ Валидированные данные: {validated_data}")

        # Обновляем пользователя
        if 'username' in validated_data:
            existing_user.username = validated_data['username']

        print("\n🔹 Результат после обновления:")
        print(f"   ID: {existing_user.id}")
        print(f"   Username: {existing_user.username}")
        print(f"   Email: {existing_user.email}")
        print(f"   Зарегистрирован: {existing_user.registered_on}")
        print(f"   Активен: {existing_user.is_active}")

        print("\n✅ Демонстрация частичного обновления завершена")
        return True  # Возвращаем значение для декоратора
    except ValidationError as e:
        print(f"   ✗ Ошибка: {e.messages}")
        print("\n✅ Демонстрация частичного обновления завершена (с ошибкой)")
        return False  # Возвращаем значение для декоратора

# ===================== ДЕМОНСТРАЦИЯ 6: ПОЛНАЯ ДЕМОНСТРАЦИЯ БЛОГА =====================

@timer
def demo_full_blog():
    """
    Комплексная демонстрация всех возможностей
    """
    print_header("🚀 ДЕМО 6: ПОЛНАЯ ДЕМОНСТРАЦИЯ БЛОГА")

    print("\n🔹 Сценарий: Создание новой статьи с комментариями")

    # Шаг 1: Создаем пользователя через валидацию
    print("\n📝 Шаг 1: Регистрация нового пользователя")
    user_input = {
        "username": "new_blogger",
        "email": "blogger@example.com"
    }

    try:
        user_schema = UserSchema()
        # load возвращает объект User, а не словарь!
        new_user = user_schema.load(user_input)
        # Присваиваем ID
        new_user.id = 3
        print(f"   ✓ Пользователь создан: {new_user}")
        # Преобразуем объект в словарь для pretty_print
        user_dict = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'registered_on': new_user.registered_on,
            'is_active': new_user.is_active
        }
        pretty_print(user_dict, "Данные пользователя")
    except ValidationError as e:
        print(f"   ✗ Ошибка: {e.messages}")
        return

    # Шаг 2: Создаем статью
    print("\n📝 Шаг 2: Создание новой статьи")
    article_input = {
        "title": "Мой первый пост о Marshmallow",
        "content": "Сегодня я начал изучать библиотеку Marshmallow. Это невероятно полезный инструмент для сериализации данных! Он помогает валидировать входящие данные и преобразовывать объекты в JSON.",
        "tags": ["marshmallow", "python", "learning"]
    }

    try:
        article_schema = ArticleSchema()
        # load возвращает словарь с данными статьи
        article_data = article_schema.load(article_input)
        # Создаем объект Article из словаря
        new_article = Article(
            3,
            article_data['title'],
            article_data['content'],
            new_user,  # new_user - это объект User
            tags=article_data.get('tags', [])
        )
        print(f"   ✓ Статья создана: {new_article}")
    except ValidationError as e:
        print(f"   ✗ Ошибка: {e.messages}")
        return

    # Шаг 3: Добавляем комментарии
    print("\n📝 Шаг 3: Добавление комментариев")

    # Создаем другого пользователя для комментария
    commenter = User(4, "curious_reader", "reader@example.com")

    comment_inputs = [
        {"text": "Отличная статья! Очень помогла новичкам."},
        {"text": "А есть продолжение?"}
    ]

    comments = []

    for i, comment_input in enumerate(comment_inputs, 1):
        try:
            # Создаем комментарий напрямую
            comment = Comment(
                i,
                comment_input['text'],
                commenter if i == 1 else new_user,
                new_article
            )
            comments.append(comment)
            print(f"   ✓ Комментарий {i} добавлен")
        except Exception as e:
            print(f"   ✗ Ошибка: {e}")

    new_article.comments = comments

    # Шаг 4: Сериализация полной структуры
    print("\n📝 Шаг 4: Итоговая структура блога")

    class FullBlogSchema(ArticleSchema):
        comments = fields.Nested(
            lambda: CommentSchema,
            many=True,
            only=('id', 'text', 'author.username', 'created_at')
        )
        author = fields.Nested(lambda: UserSchema(only=('id', 'username', 'email')))

    full_schema = FullBlogSchema()
    result = full_schema.dump(new_article)
    pretty_print(result, "Полная структура блога")

    # Статистика
    print("\n📊 Статистика:")
    print(f"   - Пользователей: 2 (автор + комментатор)")
    print(f"   - Статей: 1")
    print(f"   - Комментариев: {len(comments)}")
    print(f"   - Тегов: {len(new_article.tags)}")

    print("\n✅ Демонстрация блога завершена")