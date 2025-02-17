import faiss
import src.config
from src.config import retrieval_model , tokenizer , generation_model 

def retrieve(query, k=1):
    """
   Retrieve the k most relevant documents to the query from the FAISS index.
    - If the index has not been built or no data is found, return an empty list.
    """
    if src.config.faiss_index is None or len(src.config.global_docs) == 0:
        return []
    query_embedding = retrieval_model.encode([query], convert_to_tensor=False).astype("float32")
    distances, indices = src.config.faiss_index.search(query_embedding, k)
    retrieved_texts = [src.config.global_docs[i] for i in indices[0] if i < len(src.config.global_docs)]
    return retrieved_texts

def generate_answer(query, context):
    """
    Generate an answer based on the query and context:
        - Create a prompt, tokenize it, and call the BART model to generate the answer.  
        - Then, decode the output to return the final answer.
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
