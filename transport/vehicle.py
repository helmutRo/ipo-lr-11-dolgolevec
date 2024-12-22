from uuid import uuid4

class Vehicle:
    def __init__(self, capacity: int):
        self.vehicle_id = str(uuid4())  # генерируем ID транспорта
        self.capacity = capacity  # грузоподъёмность
        self.current_load = 0  # текущая загрузка
        self.clients_list = []  # список клиентов чьи грузы загружены

    def load_cargo(self, client):
        self.current_load += client.cargo_weight

    def __str__(self):
        return f"id: {self.vehicle_id}\nГрузоподъемность: {self.capacity}\nТекущая загрузка: {self.current_load}"
