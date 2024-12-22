import os
import json
from transport import func 
from transport.client import Client
from transport.van import Van
from transport.ship import Ship
from transport.transport_company import TransportCompany

# Функция для проверки и создания файлов, если они не существуют
def ensure_file_exists(file_path, default_data=None):
    base_path = os.path.dirname(os.path.realpath(__file__))  # Получаем путь до текущего файла
    full_path = os.path.join(base_path, 'transport', file_path)  # Строим путь к файлу относительно текущего каталога
    
    if not os.path.exists(full_path):
        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(default_data if default_data is not None else [], file, indent=4, ensure_ascii=False)


# Функция сохранения транспорта в файл
def save_transport_to_file(vehicles):
    ensure_file_exists('transport/transport.json')  # Убедимся, что файл существует
    transport_data = []
    for vehicle in vehicles:
        vehicle_info = {
            "id": vehicle.vehicle_id,
            "capacity": vehicle.capacity,
            "current_load": vehicle.current_load,
            "client_list": [client.name for client in vehicle.clients_list] 
        }
        transport_data.append(vehicle_info)

    with open('transport/transport.json', 'w', encoding='utf-8') as file:
        json.dump(transport_data, file, indent=4, ensure_ascii=False)

# Функция для отображения списка транспортных средств
def list_vehicles():
    ensure_file_exists('transport/transport.json')  # Убедимся, что файл существует
    with open('transport/transport.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for vehicle in data:
            print(f"ID: {vehicle['id']}, Грузоподъемность: {vehicle['capacity']}, Загруженность: {vehicle['current_load']}")

# Функция ввода клиента
def input_client():
    name = input("Введите имя клиента: ")
    
    # Валидация веса груза
    while True:
        try:
            cargo_weight = float(input("Введите вес груза клиента (в тоннах): "))
            if cargo_weight <= 0:
                print("Ошибка: вес груза должен быть положительным числом.")
            else:
                break
        except ValueError:
            print("Ошибка: введено не число. Пожалуйста, введите корректное значение для веса груза.")
    
    # Валидация VIP статуса
    while True:
        is_vip_input = input("Есть ли у клиента VIP статус? (да/нет): ").strip().lower()
        if is_vip_input == 'да' or is_vip_input == 'нет':
            is_vip = is_vip_input == 'да'
            break
        else:
            print("Ошибка: Пожалуйста, введите 'да' или 'нет' для VIP статуса.")
    
    # Создание клиента и добавление в список
    client = Client(name, cargo_weight, is_vip)
    func.add_to_client_list(client.add())
    
    return client


# Функция ввода транспортного средства
def input_vehicle():
    vehicle_type = input("Введите тип транспортного средства (фургон/судно): ").strip().lower()
    
    if vehicle_type not in ["фургон", "судно"]:
        print("Ошибка: некорректный тип транспортного средства. Введите 'фургон' или 'судно'.")
        return None
    
    while True:
        try:
            capacity = float(input("Введите грузоподъемность транспортного средства (в тоннах): "))
            if capacity <= 0:
                print("Ошибка: грузоподъемность должна быть положительным числом.")
            else:
                break
        except ValueError:
            print("Ошибка: введено не число. Пожалуйста, введите корректное значение.")

    if vehicle_type == "фургон":
        is_refrigerated = input("Нужен ли холодильник? (да/нет): ").strip().lower() == 'да'
        return Van(capacity, is_refrigerated)
    elif vehicle_type == "судно":
        name = input("Введите название судна: ")
        return Ship(capacity, name)
    else:
        print("Некорректный тип транспортного средства.")
        return None


# Функция проверки уникальности ID транспортного средства
def is_vehicle_id_unique(vehicle_id):
    ensure_file_exists('transport/transport.json')  # Убедимся, что файл существует
    with open('transport/transport.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for vehicle in data:
            if vehicle['id'] == vehicle_id:
                return False
    return True

# Функция добавления транспортного средства в список
def add_vehicle_to_list(vehicle):
    ensure_file_exists('transport/transport.json')  # Убедимся, что файл существует
    with open('transport/transport.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    if is_vehicle_id_unique(vehicle.vehicle_id):
        new_vehicle = {
            "id": vehicle.vehicle_id,
            "capacity": vehicle.capacity,
            "current_load": vehicle.current_load,
            "client_list": [client.name for client in vehicle.clients_list]
        }
        data.append(new_vehicle)
        with open('transport/transport.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Транспортное средство добавлено.")
    else:
        print("Ошибка: транспортное средство с таким ID уже существует.")

# Главное меню программы
def menu(company):
    while True:
        action = input("1 - Добавить клиента \n2 - Добавить транспорт\n3 - Распределить грузы \n4 - Вывести список транспорта \n5 - Выход\n")
        if action == '1':
            client = input_client()
            company.add_client(client)
            print(f"Клиент {client.name} добавлен.")
        elif action == '2':
            vehicle = input_vehicle()
            if vehicle:
                add_vehicle_to_list(vehicle)
            else:
                print("Ошибка при добавлении транспортного средства.")
        elif action == '3':
            company.optimize_cargo_distribution()
        elif action == '4':
            print("\nСписок всех транспортных средств:")
            list_vehicles()
        elif action == '5':
            print("Выход из программы.")
            break
        else:
            print("Неверная команда, попробуйте снова.")

# Основная функция
def main():
    ensure_file_exists('transport/transport.json')  # Убедимся, что файл существует
    ensure_file_exists('transport/clients.json')    # Убедимся, что файл клиентов существует
    company_name = input("Введите название компании: ")
    company = TransportCompany(company_name)
    menu(company)

if __name__ == "__main__":
    main()
