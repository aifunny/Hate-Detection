
import json

"用于抽取模型生成的预测结果"
# 输入和输出文件路径
input_file = 'generated_predictions20.jsonl'
output_file = 'predictions20.txt'

# 读取 jsonl 并提取 predict 字段
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        if not line.strip():
            continue
        data = json.loads(line)
        predict = data.get('predict', '').strip()
        if predict:
            outfile.write(predict + '\n')