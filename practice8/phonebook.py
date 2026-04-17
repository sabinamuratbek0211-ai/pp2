from connect import *


def menu():
    create_table()

    while True:
        print("\n--- PhoneBook Menu (Practice 8) ---")
        print("1. Загрузить из CSV")
        print("2. Добавить/Обновить контакт (Upsert)")
        print("3. Показать контакты (с пагинацией)")
        print("4. Поиск (через SQL-функцию)")
        print("5. Удалить контакт (через процедуру)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        # 1. CSV upload
        if choice == '1':
            try:
                upload_from_csv('contacts.csv')
                print("CSV загружен успешно!")
            except Exception as e:
                print("Ошибка загрузки CSV:", e)

        # 2. Upsert
        elif choice == '2':
            try:
                name = input("Имя: ")
                phone = input("Телефон: ")
                upsert_contact(name, phone)
                print("Контакт добавлен/обновлён!")
            except Exception as e:
                print("Ошибка:", e)

        # 3. Pagination
        elif choice == '3':
            try:
                limit = int(input("Сколько контактов показать? "))
                offset = int(input("Сколько пропустить (с какого начать)? "))

                rows = get_paged_contacts(limit, offset)

                if rows:
                    for row in rows:
                        print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
                else:
                    print("Нет данных или ошибка подключения.")

            except ValueError:
                print("Ошибка: введите числа!")
            except Exception as e:
                print("Ошибка базы данных:", e)

        # 4. Search function
        elif choice == '4':
            try:
                pattern = input("Введите часть имени или телефона: ")
                results = search_with_function(pattern)

                if results:
                    for row in results:
                        print(f"Имя: {row[0]} | Тел: {row[1]}")
                else:
                    print("Ничего не найдено.")

            except Exception as e:
                print("Ошибка поиска:", e)

        # 5. Delete procedure
        elif choice == '5':
            try:
                val = input("Введите имя или телефон для удаления: ")
                delete_via_procedure(val)
                print("Контакт удалён (если существовал).")
            except Exception as e:
                print("Ошибка удаления:", e)

        # Exit
        elif choice == '0':
            print("Пока!")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    menu()