class Client:
    def __init__(self, name: str, cargo_weight: int, is_vip: bool = False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

    def add(self):
        return {'name': self.name, 'cargo_weight': self.cargo_weight, 'is_vip': self.is_vip}

    def __str__(self):
        return f"Имя: {self.name}, Вес груза: {self.cargo_weight} тонн, VIP: {self.is_vip}"
