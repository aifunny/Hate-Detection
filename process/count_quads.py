import json

def parse_output(output_str):
    """
    解析 output 字符串为四元组列表
    """
    outputs = output_str.strip().split('[SEP]')
    tuples = []
    for out in outputs:
        out = out.replace('[END]', '').strip()
        parts = [p.strip() for p in out.split('|')]
        if len(parts) == 4:
            tuples.append(tuple(parts))
    return tuples

def count_total_quadruples(data):
    total = 0
    for item in data:
        output = item.get("output", "")
        tuples = parse_output(output)
        total += len(tuples)
    return total


if __name__ == "__main__":
    input_file = "train.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_quadruples = count_total_quadruples(data)
    print(f"四元组总数: {total_quadruples}")
