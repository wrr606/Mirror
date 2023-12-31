import json

def add_district( name, new_data):
    try:
        with open('memorandum.json', 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
    except FileNotFoundError:
        load_dict = {}
    districts = load_dict.get(name, [])
    districts.append(new_data)
    load_dict[name] = districts
    with open('memorandum.json', 'w', encoding='utf-8') as f2:
        json.dump(load_dict, f2, ensure_ascii=False, indent=2)

def remove_value(name, value_to_remove):
    try:
        with open('memorandum.json', 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
    except FileNotFoundError:
        print("JSON 文件不存在")
        return

    if name in load_dict:
        data_list = load_dict[name]
        if value_to_remove in data_list:
            data_list.remove(value_to_remove)
            print(f"成功刪除 {name} 中的值: {value_to_remove}")
        else:
            print(f"{value_to_remove} 不存在於 {name} 的值中")
    else:
        print(f"{name} 不存在於數據中")

    with open('memorandum.json', 'w', encoding='utf-8') as f2:
        json.dump(load_dict, f2, ensure_ascii=False, indent=2)
