import json

def add_to_client_list(info):
    with open('transport/clients.json', "r", encoding='utf-8') as file:
        data = json.load(file)
    data.append(info)
    with open('transport/clients.json', "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=True)

def add_to_transport_list(info):
    with open('transport/transport.json', "r", encoding='utf-8') as file:
        data = json.load(file)
    data.append(info)
    with open('transport/transport.json', "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=True)
