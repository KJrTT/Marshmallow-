import sys
from logic import (
    demo_basic_serialization,
    demo_validation,
    demo_nested_structures,
    demo_custom_fields,
    demo_partial_update,
    demo_full_blog
)
from utils import print_separator, print_header


def show_menu():
    """
    Отображение главного меню
    """
    print("\n" + "=" * 60)
    print("📦 MARSHMALLOW ДЕМОНСТРАЦИОННЫЙ ПРОЕКТ".center(60))
    print("=" * 60)
    print("1. 📄 Базовая сериализация (объект → JSON)")
    print("2. ✅ Валидация данных (JSON → объект)")
    print("3. 🔗 Вложенные структуры (автор, статьи, комментарии)")
    print("4. ⚙️ Кастомные поля и хуки")
    print("5. ✏️ Частичное обновление (partial)")
    print("6. 🚀 Полная демонстрация блога")
    print("0. ❌ Выход")
    print("-" * 60)
    return input("👉 Выберите демонстрацию (0-6): ").strip()


def main():
    """
    Главная функция приложения
    """
    print_header("🎓 УЧЕБНЫЙ ПРОЕКТ: ДЕМОНСТРАЦИЯ MARSHMALLOW")
    print("\nДобро пожаловать! Это приложение демонстрирует возможности")
    print("библиотеки Marshmallow для сериализации и валидации данных.")

    while True:
        choice = show_menu()

        if choice == "1":
            demo_basic_serialization()
        elif choice == "2":
            demo_validation()
        elif choice == "3":
            demo_nested_structures()
        elif choice == "4":
            demo_custom_fields()
        elif choice == "5":
            demo_partial_update()
        elif choice == "6":
            demo_full_blog()
        elif choice == "0":
            print("\n👋 До свидания! Спасибо за использование демонстрации.")
            sys.exit(0)
        else:
            print("\n❌ Неверный ввод. Пожалуйста, выберите цифру от 0 до 6.")

        input("\n⏎ Нажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем. До свидания!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        print("Пожалуйста, сообщите об этом разработчику.")
        sys.exit(1)