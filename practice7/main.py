from phonebook import *

def menu():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Загрузить из CSV")
        print("2. Добавить контакт вручную")
        print("3. Показать все контакты")
        print("4. Поиск по имени")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            upload_from_csv('contacts.csv')
        elif choice == '2':
            name = input("Имя: ")
            phone = input("Телефон: ")
            insert_contact(name, phone)
        elif choice == '3':
            for row in get_contacts():
                print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
        elif choice == '4':
            name = input("Введите имя для поиска: ")
            for row in get_contacts(name):
                print(row)
        elif choice == '5':
            name = input("Кого удалить?: ")
            delete_contact(name)
        elif choice == '0':
            break

if __name__ == "__main__":
    menu()