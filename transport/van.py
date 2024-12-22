from transport.vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, capacity: float, is_refrigerated: bool):
        super().__init__(capacity)
        self.is_refrigerated = is_refrigerated

    def add(self):
        return {'id': self.vehicle_id, 'capacity': self.capacity, 'current_load': self.current_load, 'client_list': self.clients_list}

    def __str__(self):
        return f"Фургон, {super().__str__()}, Холодильник: {'Да' if self.is_refrigerated else 'Нет'}"
