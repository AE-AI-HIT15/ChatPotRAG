"""
funsion :
Xác lập các biến cấu hình dùng chung.
Tạo thư mục lưu file, khởi tạo mô hình chuyển đổi văn bản thành vector và mô hình sinh văn bản.
"""
import os
import faiss
from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BartForConditionalGeneration

# Danh sách lưu trữ tất cả văn bản và FAISS index
global_docs = []
faiss_index = None

# Thư mục lưu trữ file upload
uploadfile_local = 'uploaded_files'
os.makedirs(uploadfile_local, exist_ok=True)

# Khởi tạo mô hình tạo embeddings (Retrieval)
retrieval_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Khởi tạo mô hình BART cho sinh câu trả lời
bart_model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(bart_model_name)
generation_model = BartForConditionalGeneration.from_pretrained(bart_model_name)

# Lịch sử các câu hỏi và tên file đã upload
query_history = []
file_name_history = []
