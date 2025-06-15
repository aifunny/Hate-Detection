import json
"用于构建json格式的数据进行F1分数的计算，因为txt不好对应抽取"

def txt_to_json(txt_path, json_path):
    data = []

    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        line = line.strip()  # 去除换行符和多余空格
        if line:  # 跳过空行
            data.append({
                "id": idx,
                "output": line
            })

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 示例使用
txt_to_json('predictions10.txt', 'predictions10.json')