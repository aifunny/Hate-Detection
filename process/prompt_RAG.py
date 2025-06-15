import json
import faiss
import jieba
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# ========= 配置路径和模式 =========
train_file = "train.json"
test_file = "test1.json"
output_file = "enhanced_test2.json"
K = 3  # top-K 相似样本数
use_bm25 = True  # 切换检索方式：True=BM25，False=向量检索（FAISS）

# ========= 加载训练数据 =========
with open(train_file, "r", encoding="utf-8") as f:
    train_data = json.load(f)

train_inputs = [x["content"] for x in train_data]
train_outputs = [x["output"] for x in train_data]

# ========= 检索模块构建 =========
if use_bm25:
    print("使用 BM25 检索")
    tokenized_corpus = [jieba.lcut(text) for text in train_inputs]
    bm25 = BM25Okapi(tokenized_corpus)
else:
    print("使用向量检索（FAISS）")
    encoder = SentenceTransformer("BAAI/bge-large-zh-v1.5")
    train_embeddings = encoder.encode(train_inputs, convert_to_numpy=True, normalize_embeddings=True)
    dimension = train_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(train_embeddings)

# ========= 加载测试数据 =========
with open(test_file, "r", encoding="utf-8") as f:
    test_data = json.load(f)

test_inputs = [x["content"] for x in test_data]

# ========= 相似样本检索 =========
topk_indices = []
if use_bm25:
    for text in test_inputs:
        tokenized_query = jieba.lcut(text)
        scores = bm25.get_scores(tokenized_query)
        topk = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:K]
        topk_indices.append(topk)
else:
    test_embeddings = encoder.encode(test_inputs, convert_to_numpy=True, normalize_embeddings=True)
    _, topk_result = index.search(test_embeddings, K)
    topk_indices = topk_result.tolist()

# ========= 构造增强提示结构 =========
base_instruction = (
    "你是一个审查专家，请从输入文本中提取所有仇恨言论四元组,格式如下：\n"
    "评论对象 | 论点 | 目标群体 | 是否仇恨 [END]\n"
    "评论对象和论点从原句中直接抽取不做变化，评论对象可以为 'NULL'，如果存在多个四元组，它们之间用 [SEP] 分隔。\n"
    "目标群体只允许以下几类，并附注如下：\n"
    " - Racism：涉及种族、民族、肤色\n"
    " - Sexism：涉及性别歧视、贬低女性或男性\n"
    " - Region：基于地域、国家、省份的偏见\n"
    " - LGBTQ：针对同性恋、跨性别者等性少数群体\n"
    " - others：如宗教歧视、身体歧视等\n"
    " - non-hate：中性或正向评论，不具有仇恨倾向\n"
    "是否仇恨 只可为 hate 或 non-hate。\n"
    "注意可能存在多个标签组合，如 Sexism, Racism 等。\n"
    "下面有相似的提取实例：\n"
)

enhanced_data = []
for i, test_ex in enumerate(test_data):
    fewshot = ""
    for idx in topk_indices[i]:
        fewshot += f"输入：{train_inputs[idx]}\n输出：{train_outputs[idx]}\n\n"

    full_instruction = base_instruction + fewshot + "现在请处理："
    full_input = test_ex["content"]

    enhanced_data.append({
        "instruction": full_instruction,
        "input": full_input,
        "output": ""
    })

# ========= 保存为 JSONL =========
with open(output_file, "w", encoding="utf-8") as f:
    for item in enhanced_data:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")

print(f"已保存增强提示文件：{output_file}，共 {len(enhanced_data)} 条样本。")
