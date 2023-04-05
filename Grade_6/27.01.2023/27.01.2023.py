import json


def func(num):
    return num * 2


data = {
    "key": ['value', 2, 3],
    'asd': {
        'asd': 321,
        'key2': (1, 2, 3)
    },
    # 'func': func
}

with open('../Undated/data.json', mode='w', encoding='utf-8') as file:
    json.dump(data, file)

with open('../Undated/data.json', mode='r', encoding='utf-8') as file:
    json_data = json.load(file)

print(json_data)
