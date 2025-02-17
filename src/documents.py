import os
import pandas as pd
import faiss
from src.config import global_docs, uploadfile_local, retrieval_model
import src.config  

def build_faiss_index(docs):
    if not docs:
        print("Lỗi: Danh sách tài liệu rỗng, không thể xây dựng FAISS index.")
        return
    
    embeddings = retrieval_model.encode(docs, convert_to_tensor=False).astype("float32")
    dimension = embeddings.shape[1]

    # **Update the FAISS index in config.py**
    src.config.faiss_index = faiss.IndexFlatL2(dimension)
    src.config.faiss_index.add(embeddings)
    
    

def load_documents_from_csv(csv_path, text_column="content"):
    """
    **Iterate through CSV files in the `uploadfile_local` directory, read the `text_column`,**  
        - Update `global_docs`.  
        - Then, build the FAISS index.
    """
    global global_docs
    global_docs = []
    for file in os.listdir(uploadfile_local):
        if file.endswith('.csv'):
            csv_file = os.path.join(uploadfile_local, file)
            df = pd.read_csv(csv_file)
            new_docs = df[text_column].dropna().tolist()
            global_docs.extend(new_docs)  # Cập nhật toàn bộ danh sách tài liệu
    build_faiss_index(global_docs)


def load_documents_from_txt(txt_file):
    """
    Iterate through TXT files in the `uploadfile_local` directory,  
        - Read the content line by line and split the text into segments when encountering a period.  
        - If valid data is found, build the FAISS index.
    """
    global global_docs
    docs = []
    
    with open(txt_file, "r", encoding="utf-8") as txt_f:
        new_docs = ""
        for line in txt_f:
            line = line.strip()
            if not line:
                continue
            for char in line:
                new_docs += char
                if char == ".":
                    docs.append(new_docs.strip())
                    new_docs = ""
    
    if docs:
        global_docs.extend(docs)  
        build_faiss_index(global_docs)
        
    else:
        print("Lỗi: Không có dữ liệu hợp lệ để xây dựng FAISS index.")
