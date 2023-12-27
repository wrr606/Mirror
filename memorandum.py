

import json

def add_district(name, new_data):

    try:
        # 讀取現有的 JSON 數據
        with open('test.json', 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
    except FileNotFoundError:
        # 如果檔案不存在，建立一個新的字典
        load_dict = {}

    # 取得姓名對應的資料列表，如果不存在則建立一個新的空列表
    districts = load_dict.get(name, [])

    # 向資料列表中添加新的資料
    districts.append(new_data)

    # 更新字典
    load_dict[name] = districts

    # 將更新後面的資料寫回JSON文件
    with open('test.json', 'w', encoding='utf-8') as f2:
        json.dump(load_dict, f2, ensure_ascii=False, indent=2)

