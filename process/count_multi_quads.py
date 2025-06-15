import json

def count_sep_samples(data):
    count = 0
    for item in data:
        output = item.get("output", "")
        if "[SEP]" in output:
            count += 1
    return count

# 读取JSON数据
if __name__ == "__main__":
    input_file = "train.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    sep_count = count_sep_samples(data)

    print(f"包含 [SEP] 分隔符的样本数量（即多四元组样本）: {sep_count}")



# from collections import Counter
#
# def count_sep_occurrences(txt_path):
#     counter = Counter()
#
#     with open(txt_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             sep_count = line.count('[SEP]')
#             counter[sep_count] += 1
#
#     return counter
#
# # 示例使用
# txt_file = 'Truth.txt'
# sep_counter = count_sep_occurrences(txt_file)
#
# # 打印所有统计结果（按 [SEP] 次数升序）
# for sep_times in sorted(sep_counter):
#     print(f"[SEP] 出现 {sep_times} 次的行数: {sep_counter[sep_times]}")
# import json
# from collections import Counter
#
# def count_sep_in_json_outputs(json_path):
#     counter = Counter()
#
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)  # 假设是一个 list，每个元素是一个字典
#
#     for item in data:
#         output = item.get("output", "")
#         sep_count = output.count("[SEP]")
#         counter[sep_count] += 1
#
#     return counter
#
#
# json_file = 'train.json'
# sep_counts = count_sep_in_json_outputs(json_file)
#
# # 输出统计结果
# for count in sorted(sep_counts):
#     print(f'"output" 中 [SEP] 出现 {count} 次的样例数量: {sep_counts[count]}')
