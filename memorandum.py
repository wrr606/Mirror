import json

def add_district( name, new_data):
    try:
        # 讀取現有的 JSON 數據
        with open('memorandum.json', 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
    except FileNotFoundError:
        # 如果檔案不存在，建立一個新的字典
        load_dict = {}

    # 取得姓名对应的数据列表，如果不存在则创建一个新的空列表
    districts = load_dict.get(name, [])

    # 向数据列表中添加新的数据
    districts.append(new_data)

    # 更新字典
    load_dict[name] = districts

    # 将更新后的数据写回JSON文件
    with open('memorandum.json', 'w', encoding='utf-8') as f2:
        json.dump(load_dict, f2, ensure_ascii=False, indent=2)

def remove_value(name, value_to_remove):
    try:
        # 读取现有的 JSON 数据
        with open('memorandum.json', 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
    except FileNotFoundError:
        print("JSON 文件不存在")
        return

    # 检查姓名是否存在于字典中
    if name in load_dict:
        # 获取姓名对应的数据列表
        data_list = load_dict[name]

        # 检查要删除的值是否存在于列表中
        if value_to_remove in data_list:
            # 从列表中删除指定的值
            data_list.remove(value_to_remove)
            print(f"成功删除 {name} 中的值: {value_to_remove}")
        else:
            print(f"{value_to_remove} 不存在于 {name} 的值中")
    else:
        print(f"{name} 不存在于数据中")

    # 将更新后的数据写回JSON文件
    with open('memorandum.json', 'w', encoding='utf-8') as f2:
        json.dump(load_dict, f2, ensure_ascii=False, indent=2)