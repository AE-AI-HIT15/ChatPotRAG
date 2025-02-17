import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models import AskResponse , AskRequest
from ask import ask_endpoint
from documents import load_documents_from_csv, load_documents_from_txt
from config import uploadfile_local, file_name_history, query_history

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.options("/ask")
async def options_handler():
    return {"message": "OPTIONS request accepted"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint for users to upload files (CSV or TXT):

        +Save the file to the uploadfile_local directory.
        +Record the file name in file_name_history.
        +Call load_documents_from_txt or load_documents_from_csv based on the file format.
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
    Endpoint to receive questions from users.
    """
  
    response = ask_endpoint(request.query)
    return response

@app.get('/history_question')
async def get_history():
    """ Return the history of questions that have been submitted. """
    return query_history

@app.get('/file_name')
async def get_file_name():
    """ Return the list of file names that have been uploaded. """
    return file_name_history
