import json

data = {
    "key": ['value', 2, 3],
    'asd': {
        'asd': 321
    }
}

with open('data.json', mode='w', encoding='utf-8') as file:
    json.dump(data, file)

with open('data.json', mode='r', encoding='utf-8') as file:
    json_data = json.load(file)

print(json_data)


