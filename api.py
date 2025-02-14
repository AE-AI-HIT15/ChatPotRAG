import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models import AskResponse , AskRequest
from ask import ask_endpoint
from documents import load_documents_from_csv, load_documents_from_txt
from config import uploadfile_local, file_name_history, query_history

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Chấp nhận tất cả origin
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức
    allow_headers=["*"],  # Chấp nhận tất cả header
)

@app.options("/ask")
async def options_handler():
    return {"message": "OPTIONS request accepted"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint để người dùng upload file (CSV hoặc TXT).
    - Lưu file vào thư mục uploadfile_local.
    - Ghi nhận tên file vào file_name_history.
    - Gọi load_documents_from_txt hoặc load_documents_from_csv dựa trên định dạng file.
    """
    file_path = os.path.join(uploadfile_local, file.filename)
    file_name_history.append(file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if file.filename.endswith('.txt'):
        load_documents_from_txt(file_path)
    elif file.filename.endswith('.csv'):
        load_documents_from_csv(file_path)
    return {"message": f"Tệp {file.filename} đã được tải lên và xử lý."}

@app.post("/ask", response_model=AskResponse)
async def submit_question(request: AskRequest ):
    """
    Endpoint nhận câu hỏi từ người dùng.
    """
  
    response = ask_endpoint(request.query)
    return response

@app.get('/history_question')
async def get_history():
    """ Trả về lịch sử các câu hỏi đã được gửi. """
    return query_history

@app.get('/file_name')
async def get_file_name():
    """ Trả về danh sách tên file đã được upload. """
    return file_name_history
