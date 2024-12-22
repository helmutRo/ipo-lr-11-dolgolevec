import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from transport.client import Client
from transport.van import Van
from transport.ship import Ship
from transport.transport_company import TransportCompany
class TransportApp:
    #конструктор приложения
    def __init__(self, root, company):
        self.root = root # Глав окно
        self.company = company# Компания
        self.root.title(f"{self.company.name} - управление транспортом") # Название окна
        self.load_data()# Загрузка данных из файлов
        self.create_widgets()
    #Загрузка данных из файлов
    def load_data(self):
        #проверка и загрузка данных клиентов
        if os.path.exists("clients.json"):
            with open("clients.json", "r") as f:
                clients_data = json.load(f)
                for client_data in clients_data:
                    client = Client(client_data['name'], client_data['cargo_weight'], client_data['is_vip'])
                    self.company.add_client(client)
        #проверка и загрузка данных транспорта
        if os.path.exists("transport.json"):
            with open("transport.json", "r") as f:
                transport_data = json.load(f)
                for vehicle_data in transport_data:
                    if vehicle_data['type'] == 'Van':
                        vehicle = Van(vehicle_data['capacity'], vehicle_data['is_refrigerated'])
                    elif vehicle_data['type'] == 'Ship':
                        vehicle = Ship(vehicle_data['capacity'], vehicle_data['name'])
                    self.company.add_vehicle(vehicle)
    #сохранение данных в файлы
    def save_data(self):
        clients_data = [{'name': client.name, 'cargo_weight': client.cargo_weight, 'is_vip': client.is_vip} for client in self.company.clients]
        with open("clients.json", "w") as f:
            json.dump(clients_data, f)
        #сохранение данных транспорта в файл
        transport_data = [{'type': type(vehicle).__name__, 'capacity': vehicle.capacity, 'name': getattr(vehicle, 'name', ''), 'is_refrigerated': getattr(vehicle, 'is_refrigerated', False)} for vehicle in self.company.vehicles]
        with open("transport.json", "w") as f:
            json.dump(transport_data, f)
    #создание эл интерфейса
    def create_widgets(self):
        #создание глав меню
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Меню", menu=file_menu)
        file_menu.add_command(label="Экспорт результата", command=self.export_results)
        file_menu.add_command(label="О программе", command=self.show_about)
        #кнопки управления объектами
        control_frame = tk.Frame(self.root)
        control_frame.pack(padx=10, pady=10)
        self.add_client_button = tk.Button(control_frame, text="Добавить клиента", command=self.add_client)
        self.add_client_button.grid(row=0, column=0, padx=5, pady=5)
        self.add_vehicle_button = tk.Button(control_frame, text="Добавить транспорт", command=self.add_vehicle)
        self.add_vehicle_button.grid(row=0, column=1, padx=5, pady=5)
        self.optimize_cargo_button = tk.Button(control_frame, text="Распределить грузы", command=self.optimize_cargo)
        self.optimize_cargo_button.grid(row=0, column=2, padx=5, pady=5)
        #всплывающие подсказки
        self.add_client_button.bind("<Enter>", self.show_tooltip_add_client)
        self.add_vehicle_button.bind("<Enter>", self.show_tooltip_add_vehicle)
        self.optimize_cargo_button.bind("<Enter>", self.show_tooltip_optimize_cargo)
        #таблицы для отображения данных
        self.client_listbox = tk.Listbox(self.root, width=50, height=10)
        self.client_listbox.pack(padx=10, pady=5)
        self.vehicle_listbox = tk.Listbox(self.root, width=50, height=10)
        self.vehicle_listbox.pack(padx=10, pady=5)
        #редактирование и удаление
        self.client_listbox.bind("<Double-1>", self.edit_client)  #двойной щелчок на клиенте
        self.vehicle_listbox.bind("<Double-1>", self.edit_vehicle)
        self.delete_button = tk.Button(self.root, text="Удалить", command=self.delete_object)
        self.delete_button.pack(padx=10, pady=5)
    #всплывающая подсказка для добавления клиента
    def show_tooltip_add_client(self, event):
        self.show_tooltip("Добавить нового клиента")
    #всплывающая подсказка для добавления транспорта
    def show_tooltip_add_vehicle(self, event):
        self.show_tooltip("Добавить новое транспортное средство")
    #всплывающая подсказка для распределения грузов
    def show_tooltip_optimize_cargo(self, event):
        self.show_tooltip("Оптимизировать распределение грузов")
    #показает всплывающую подсказку
    def show_tooltip(self, message):
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.geometry(f"+{self.root.winfo_pointerx()+10}+{self.root.winfo_pointery()+10}")
        label = tk.Label(tooltip, text=message, bg="#D3D3D3", padx=10, pady=5)  # Используем светло-серый цвет
        label.pack()
        # Закрыть подсказку через 1 секунду
        tooltip.after(1000, tooltip.destroy)
    #добав нового клиента
    def add_client(self):
        name = simpledialog.askstring("Добавить клиента", "Введите имя клиента:")
        cargo_weight = simpledialog.askfloat("Добавить клиента", "Введите вес груза (в тоннах):")
        is_vip = messagebox.askyesno("VIP статус", "Есть ли у клиента VIP статус?")
        if not name or not cargo_weight or cargo_weight <= 0:
            messagebox.showerror("Ошибка", "Неправильные данные")
            return
        client = Client(name, cargo_weight, is_vip)
        self.company.add_client(client)
        self.refresh_client_list()
        messagebox.showinfo("успех", f"клиент {name} добавлен.")
        self.save_data()
    #добав нового транспорта
    def add_vehicle(self):
        vehicle_type = simpledialog.askstring("Тип транспорта", "Выберите тип транспорта (Фургон/Судно):")
        capacity = simpledialog.askfloat("Добавить транспорт", "Введите грузоподъемность транспорта (в тоннах):")
        if vehicle_type.lower() == "фургон":
            is_refrigerated = messagebox.askyesno("Холодильник", "Нужен ли холодильник?")
            vehicle = Van(capacity, is_refrigerated)
        elif vehicle_type.lower() == "судно":
            name = simpledialog.askstring("Добавить транспорт", "Введите название судна:")
            vehicle = Ship(capacity, name)
        else:
            messagebox.showerror("Ошибка", "Некорректный тип транспорта")
            return
        self.company.add_vehicle(vehicle)
        self.refresh_vehicle_list()
        messagebox.showinfo("Успех", "Транспортное средство добавлено.")
        self.save_data()
    #редактирование данных клиента
    def edit_client(self, event):
        selected_index = self.client_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "выберете клиента для редактирования")
            return
        client = self.company.clients[selected_index[0]]
        name = simpledialog.askstring("Редактировать клиента", "Введите новое имя клиента:", initialvalue=client.name)
        cargo_weight = simpledialog.askfloat("Редактировать клиента", "Введите новый вес груза (в тоннах):", initialvalue=client.cargo_weight)
        is_vip = messagebox.askyesno("VIP статус", "Есть ли у клиента VIP статус?", default=client.is_vip)
        if not name or not cargo_weight or cargo_weight <= 0:
            messagebox.showerror("Ошибка", "Некорректные данные")
            return
        client.name = name
        client.cargo_weight = cargo_weight
        client.is_vip = is_vip
        self.refresh_client_list()
        self.save_data()
    #редактирование данных транспорта
    def edit_vehicle(self, event):
        selected_index = self.vehicle_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "выберете транспорт для редактирования")
            return
        vehicle = self.company.vehicles[selected_index[0]]
        vehicle_type = simpledialog.askstring("Редактировать транспорт", "Выберите тип транспорта (Фургон/Судно):", initialvalue=type(vehicle).__name__.lower())
        capacity = simpledialog.askfloat("Редактировать транспорт", "Введите новую грузоподъемность (в тоннах):", initialvalue=vehicle.capacity)
        if vehicle_type.lower() == "фургон":
            is_refrigerated = messagebox.askyesno("Холодильник", "Нужен ли холодильник?", default=vehicle.is_refrigerated)
            vehicle = Van(capacity, is_refrigerated)
        elif vehicle_type.lower() == "судно":
            name = simpledialog.askstring("Редактировать транспорт", "Введите новое название судна:", initialvalue=vehicle.name)
            vehicle = Ship(capacity, name)
        else:
            messagebox.showerror("Ошибка", "Некорректный тип транспорта")
            return
        self.company.vehicles[selected_index[0]] = vehicle
        self.refresh_vehicle_list()
        self.save_data()
    #обновление списка клиентов
    def refresh_client_list(self):
        self.client_listbox.delete(0, tk.END)
        for client in self.company.clients:
            self.client_listbox.insert(tk.END, f"{client.name}, {client.cargo_weight} тонн")
    #обновление списка транспорта
    def refresh_vehicle_list(self):
        self.vehicle_listbox.delete(0, tk.END)
        for vehicle in self.company.vehicles:
            self.vehicle_listbox.insert(tk.END, f"{vehicle.vehicle_id}, {vehicle.capacity} тонн")
    # оптимизация распределения грузов
    def optimize_cargo(self):
        self.company.optimize_cargo_distribution()
        messagebox.showinfo("Распределение", "Грузы распределены.")
        self.refresh_vehicle_list()
    #лобав результатов распределения в файл
    def export_results(self):
        results = self.company.get_distribution_results()
        with open("cargo_distribution_results.json", "w") as f:
            json.dump(results, f)
        messagebox.showinfo("Экспорт", "Результаты успешно экспортированы.")
    #показать информацию о программе
    def show_about(self):
        messagebox.showinfo("О программе", "ЛР 11\nВариант: 123\nФИО разработчика: Иванов И.И.")
    #удаление
    def delete_object(self):
        selected_client_index = self.client_listbox.curselection()
        selected_vehicle_index = self.vehicle_listbox.curselection()
        if selected_client_index:
            client = self.company.clients[selected_client_index[0]]
            self.company.clients.remove(client)
            self.refresh_client_list()
            messagebox.showinfo("Удаление", f"Клиент {client.name} удален.")
        if selected_vehicle_index:
            vehicle = self.company.vehicles[selected_vehicle_index[0]]
            self.company.vehicles.remove(vehicle)
            self.refresh_vehicle_list()
            messagebox.showinfo("Удаление", f"Транспортное средство {vehicle.vehicle_id} удалено.")
        self.save_data()
#функция запуска
def main():
    company_name = simpledialog.askstring("Компания", "Введите название компании:")
    company = TransportCompany(company_name)
    root = tk.Tk()#глав окно
    app = TransportApp(root, company) #создание приложения
    root.mainloop() #запуск основного цикла
#проверка главного скрипта
if __name__ == "__main__":
    main()