import json

class TransportCompany:
    def __init__(self, name: str):
        self.name = name
        self.clients = []
        self.vehicles = []

    def add_client(self, client):
        self.clients.append(client)
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    
    def list_vehicles(self):
        return self.vehicles
    
    def optimize_cargo_distribution(self):
        self.clients.sort(key=lambda client: client.is_vip, reverse=True)
        
        for vehicle in self.vehicles:
            for client in self.clients:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    vehicle.load_cargo(client)
                    vehicle.clients_list.append(client)
                    print(f"Груз клиента {client.name} загружен на транспортное средство {vehicle.vehicle_id}")
                    self.clients.remove(client)
                    break
            if not self.clients:
                break
        
        if self.clients:
            print("Не все грузы удалось распределить, не хватает транспорта.")
        else:
            print("Все грузы успешно распределены по транспортным средствам.")
