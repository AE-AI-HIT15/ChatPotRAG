"""
**Function:**  
- Define common configuration variables.  
- Create a directory to store files, initialize the model for converting text into vectors, and initialize the text generation model.
"""
import os
import faiss
from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BartForConditionalGeneration

# **List to store all documents and FAISS index**
global_docs = []
faiss_index = None

# **Directory to store uploaded files**
uploadfile_local = 'uploaded_files'
os.makedirs(uploadfile_local, exist_ok=True)

# **Initialize the model for generating embeddings (Retrieval)**
retrieval_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# **Initialize the BART model for generating answers**
bart_model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(bart_model_name)
generation_model = BartForConditionalGeneration.from_pretrained(bart_model_name)

# **History of questions and uploaded file names**
query_history = []
file_name_history = []
