import json

# def build_stage1_data(data_path, out_path):
#     with open(data_path, 'r', encoding='utf-8') as f:
#         dataset = json.load(f)
#     lines = []
#     for item in dataset:
#         quadruples = item['output'].replace('[END]','').split('[SEP]')
#         ta_list = []
#         for quad in quadruples:
#             quad = quad.strip()
#             if not quad: continue
#             parts = [x.strip() for x in quad.split('|')]
#             if len(parts) < 2: continue
#             ta_list.append(f"{parts[0]} | {parts[1]}")
#         output = " [SEP] ".join(ta_list) + " [END]"
#         lines.append({
#             "instruction": "请从下述文本中抽取所有评论对象及对应观点（T-A对），格式：评论对象 | 观点 [END]，多个T-A对用[SEP]分隔。",
#             "input": item['content'],
#             "output": output
#         })
#     with open(out_path, 'w', encoding='utf-8') as f:
#         for line in lines:
#             f.write(json.dumps(line, ensure_ascii=False) + '\n')
#
# build_stage1_data('train.json', 'stage1_train.jsonl')

# def build_stage2_data(data_path, out_path):
#     with open(data_path, 'r', encoding='utf-8') as f:
#         dataset = json.load(f)
#     lines = []
#     for item in dataset:
#         quadruples = item['output'].replace('[END]','').split('[SEP]')
#         for quad in quadruples:
#             quad = quad.strip()
#             if not quad: continue
#             parts = [x.strip() for x in quad.split('|')]
#             if len(parts) != 4: continue
#             t, a, group, hate = parts
#             lines.append({
#                 "instruction": "请判断下述评论对象-论点对的目标群体和仇恨性,目标群体只包括LGBTQ、Region、Sexism、Racism、 others、non-hate，可能涉及多个目标群体，多目标群体关注Sexism, Racism这一类，格式：目标群体 | 是否仇恨。",
#                 "input": f"{t} | {a}",
#                 "output": f"{group} | {hate}"
#             })
#     with open(out_path, 'w', encoding='utf-8') as f:
#         for line in lines:
#             f.write(json.dumps(line, ensure_ascii=False) + '\n')
#
# build_stage2_data('train.json', 'stage2_train.jsonl')

import json

# PROMPT = (
#     "你是一个审查专家, 请从输入文本中提取所有仇恨言论四元组,格式如下：\n"
#     "评论对象 | 论点 | 目标群体 | 是否仇恨 [END]\n"
#     "评论对象和论点从原句中直接抽取不做变化,评论对象可以为'NULL', 如果存在多个四元组,它们之间用[SEP]分隔.\n"
#     "目标群体只包括Racism、Sexism、Region、LGBTQ、others、non-hate,或多个标签英文逗号分隔."
#     "注意长尾组合（如Sexism, Racism等）也可能出现但数量较少,目标群体中non-hate类别与是否仇恨中的non-hate对应\n"
#     "是否仇恨为hate或non-hate.\n"
#     "现在请处理文本："
# )
PROMPT = (
    "你是一个审查专家，请从输入文本中提取所有仇恨言论四元组，格式如下：\n"
    "评论对象 | 论点 | 目标群体 | 是否仇恨 [END]\n"
    "评论对象和论点从原句中直接抽取不做变化，评论对象可以为 'NULL'，如果存在多个四元组，它们之间用 [SEP] 分隔。\n"
    "目标群体只允许以下几类，并附注如下：\n"
    " - Racism：涉及种族、民族、肤色（如针对黑人、白人、亚裔、拉丁裔等）\n"
    " - Sexism：涉及性别歧视、贬低女性或男性、强化性别刻板印象\n"
    " - Region：基于地域、国家、省份、地方偏见或敌意（如地域黑、排外）\n"
    " - LGBTQ：针对同性恋、双性恋、跨性别者等性少数群体的贬损或歧视\n"
    " - others：无法归类于以上标签但仍具有歧视性或攻击性的目标群体（如宗教歧视、身体歧视、职业歧视等）\n"
    " - non-hate：中性或正向评论，不具有仇恨倾向，对应于“是否仇恨”为 non-hate\n"
    "注意可能存在多个标签组合，如 Sexism, Racism 等。\n"
    "是否仇恨 只可为 hate 或 non-hate。\n"
    "现在请处理文本："
)

input_path = "train.json"
output_path = "sft_train2.jsonl"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(output_path, "w", encoding="utf-8") as fout:
    for item in data:
        instruction = PROMPT
        input_text = item["content"]
        output_text = item["output"].strip()
        json.dump({
            "instruction": instruction,
            "input": input_text,
            "output": output_text
        }, fout, ensure_ascii=False)
        fout.write('\n')


import json

# PROMPT = (
#     "你是一个审查专家, 请从输入文本中提取所有仇恨言论四元组,格式如下：\n"
#     "评论对象 | 论点 | 目标群体 | 是否仇恨 [END]\n"
#     "评论对象和论点从原句中直接抽取不做变化,评论对象可以为'NULL', 如果存在多个四元组,它们之间用[SEP]分隔.\n"
#     "目标群体只包括Racism、Sexism、Region、LGBTQ、others、non-hate,或多个标签英文逗号分隔."
#     "注意长尾组合（如Sexism, Racism等）也可能出现但数量较少,目标群体中non-hate类别与是否仇恨中的non-hate对应\n"
#     "是否仇恨为hate或non-hate.\n"
#     "现在请处理文本："
# )
PROMPT = (
    "你是一个审查专家，请从输入文本中提取所有仇恨言论四元组，格式如下：\n"
    "评论对象 | 论点 | 目标群体 | 是否仇恨 [END]\n"
    "评论对象和论点从原句中直接抽取不做变化，评论对象可以为 'NULL'，如果存在多个四元组，它们之间用 [SEP] 分隔。\n"
    "目标群体只允许以下几类，并附注如下：\n"
    " - Racism：涉及种族、民族、肤色（如针对黑人、白人、亚裔、拉丁裔等）\n"
    " - Sexism：涉及性别歧视、贬低女性或男性、强化性别刻板印象\n"
    " - Region：基于地域、国家、省份、地方偏见或敌意（如地域黑、排外）\n"
    " - LGBTQ：针对同性恋、双性恋、跨性别者等性少数群体的贬损或歧视\n"
    " - others：无法归类于以上标签但仍具有歧视性或攻击性的目标群体（如宗教歧视、身体歧视、职业歧视等）\n"
    " - non-hate：中性或正向评论，不具有仇恨倾向，对应于“是否仇恨”为 non-hate\n"
    "注意可能存在多个标签组合，如 Sexism, Racism 等。\n"
    "是否仇恨 只可为 hate 或 non-hate。\n"
    "现在请处理文本："
)


input_path = "test1.json"
output_path = "test2.jsonl"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(output_path, "w", encoding="utf-8") as fout:
    for item in data:
        instruction = PROMPT
        input_text = item["content"]
        output_text = item["output"]
        # output_text = item["output"].strip()
        json.dump({
            "prompt": instruction + input_text,
            "chosen": output_text,

        }, fout, ensure_ascii=False)
        fout.write('\n')

