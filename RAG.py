import faiss
import config
from config import retrieval_model , tokenizer , generation_model 

def retrieve(query, k=1):
    """
    Truy xuất k văn bản gần nhất với query từ FAISS index.
    Nếu index chưa được xây dựng hoặc không có dữ liệu, trả về danh sách rỗng.
    """
    if config.faiss_index is None or len(config.global_docs) == 0:
        return []
    query_embedding = retrieval_model.encode([query], convert_to_tensor=False).astype("float32")
    distances, indices = config.faiss_index.search(query_embedding, k)
    retrieved_texts = [config.global_docs[i] for i in indices[0] if i < len(config.global_docs)]
    return retrieved_texts

def generate_answer(query, context):
    """
    Sinh câu trả lời dựa trên query và context.
    Tạo prompt, token hóa và gọi mô hình BART để sinh câu trả lời.
    Sau đó giải mã output trả về câu trả lời cuối cùng.
    """
    prompt = f"Question: {query}\nContext: {context}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = generation_model.generate(
        inputs.input_ids, 
        max_new_tokens=150,
        num_beams=30,
        early_stopping=True
    )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
