import json
from collections import Counter

# 全局统计变量（包括多目标计数器）
multi_output_count = 0
def parse_output(output_str,num):
    """
    将output字段解析成四元组列表
    每个四元组格式为：text1 | text2 | Targeted Group | Hateful
    多个四元组之间用 [SEP] 分隔，最后一个以 [END] 结尾
    """
    outputs = output_str.strip().split('[SEP]')
    parsed = []
    for out in outputs:
        out = out.replace('[END]', '').strip()
        parts = [p.strip() for p in out.split('|')]
        if len(parts) == 4:
            parsed.append((parts[0], parts[1], parts[2], parts[3]))

    # if (num == 1):
    #     print(parsed)
    return parsed

def count_labels(data):
    """
    遍历数据，统计Targeted Group和Hateful的出现频次
    同时记录包含多个四元组的样本数量
    """
    global multi_output_count
    targeted_group_counter = Counter()
    hateful_counter = Counter()

    num = 2
    for item in data:
        output = item.get("output", "")
        id = item.get("id", "")
        if(id == 4008):
            num = 1
        else:
            num = 2
        tuples = parse_output(output, num)

        if len(tuples) > 1:
            multi_output_count += 1  # 多目标样本计数

        for _, _, group, hate in tuples:
            targeted_group_counter[group] += 1
            hateful_counter[hate] += 1

        # for _, _, group, hate in tuples:
        #     for g in [g.strip() for g in group.split(',')]:
        #         targeted_group_counter[g] += 1
        #     hateful_counter[hate] += 1

    return targeted_group_counter, hateful_counter

# 主程序入口
if __name__ == "__main__":
    # json文件路径
    input_file = "./train.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    targeted_counts, hateful_counts = count_labels(data)

    print(f"包含多个四元组（多目标）的样本数量: {multi_output_count}")
    print(f"单四元组（多目标）的样本数量: {4000-multi_output_count}\n")

    print("Targeted Group 统计：")
    for key, value in targeted_counts.items():
        print(f"{key}: {value}")

    total_targeted = sum(targeted_counts.values())
    print(f"Targeted Group 总计标签次数: {total_targeted}")

    print("\nHateful 统计：")
    for key, value in hateful_counts.items():
        print(f"{key}: {value}")
