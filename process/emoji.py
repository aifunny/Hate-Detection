import json
import re
"这个是用于对于样例中表情包的影响的统计，但最终证明由于数据样例过少，影响不大，更多的是词汇含有仇恨信息"
# 加载 JSON 数据
with open('./train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 表情匹配正则（Unicode Emoji 范围）
emoji_pattern = re.compile(
    u"[\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    u"\U0001F1E0-\U0001F1FF"
    u"\u2600-\u26FF"
    u"\u2700-\u27BF]+",
    flags=re.UNICODE
)

count = 0
for item in data:
    content = item.get("content", "")
    output = item.get("output", "")

    # 条件1：判断是否包含 Unicode 表情
    if not emoji_pattern.search(content):
        continue

    # 条件2：提取第一个四元组（从开头到第一个 [SEP] 或 [END]）
    output = output.strip()
    if '[SEP]' in output:
        first_segment = output.split('[SEP]')[0].strip()
    elif '[END]' in output:
        first_segment = output.split('[END]')[0].strip()
    else:
        first_segment = output  # 极端情况下没有任何标记

    fields = [f.strip() for f in first_segment.split('|')]

    # 判断第四个字段是否是 "hate"
    if len(fields) >= 4 and fields[3].lower() == "non-hate":
        count += 1

print(f"含 Unicode 表情且第四个指标为 'hate' 的样例数量：{count}")


#
# # 加载 JSON 数据
# with open('./NLP评测/train2.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# # 限定的 emoji 字符集
# target_emojis = {'😢', '😅', '🤣', '😠', '😆', '😄'}
# # target_emojis = {'😄'}

# # 统计符合条件的样本数量
# count = 0

# for item in data:
#     content = item.get("content", "")
#     output = item.get("Q1 hateful", "")
#
#     # 条件1：content 中是否含有指定 emoji 中的任意一个
#     if not any(emoji in content for emoji in target_emojis):
#         continue
#
#     # 条件2：提取 output 的第一个四元组（以 [SEP] 或 [END] 分隔）
#     # output = output.strip()
#     # if '[SEP]' in output:
#     #     first_segment = output.split('[SEP]')[0].strip()
#     # elif '[END]' in output:
#     #     first_segment = output.split('[END]')[0].strip()
#     # else:
#     #     first_segment = output  # 极少数情况下没有 [SEP] 或 [END]
#     #
#     # fields = [f.strip() for f in first_segment.split('|')]
#     #
#     # # 判断第四个字段是否是 "hate"
#     # if len(fields) >= 4 and fields[3].lower() == "hate":
#     #     count += 1
#     if(output == "hate"):
#         count += 1
#
# print(f"含指定 emoji 且第四项为 'hate' 的样例数量：{count}")

