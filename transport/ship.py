from transport.vehicle import Vehicle

class Ship(Vehicle):
    def __init__(self, capacity: float, name: str):
        super().__init__(capacity)  # вызов конструктора родительского класса
        self.name = name  # название судна

    def __str__(self):
        # описание судна, добавляется информация о названии судна
        return super().__str__() + f", Название судна: {self.name}"
