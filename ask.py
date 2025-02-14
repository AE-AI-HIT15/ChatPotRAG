# ask.py
import re
from config import query_history
from models import AskRequest, AskResponse
from RAG import retrieve, generate_answer

def ask(request: AskRequest) -> AskResponse:
    """
    Xử lý một câu hỏi đơn lẻ:
    - Ghi nhận câu hỏi vào lịch sử.
    - Truy xuất các văn bản liên quan (k=3 và k=1).
    - Nếu không có dữ liệu, trả về thông báo lỗi.
    - Ngược lại, kết hợp context và gọi hàm sinh câu trả lời.
    """
    query = request.query
    query_history.append(query)
    
    retrieved_list = retrieve(query, k=3)
    query_fake_list = retrieve(query, k=1)
 
    if not retrieved_list:
        return AskResponse(answer="Xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi này: " + query, context="")
    
    context = " ".join(retrieved_list)
    query_fake = query_fake_list[0] if query_fake_list else query
    answer = generate_answer(query_fake, context)
    return AskResponse(answer=answer, context=context)
    
def ask_endpoint(request: str) -> AskResponse:
    """
    Xử lý chuỗi câu hỏi chứa nhiều câu:
    - Phân tách các câu dựa trên dấu chấm, chấm hỏi, chấm than.
    - Với mỗi câu, gọi hàm ask để lấy câu trả lời.
    - Nối kết kết quả của các câu và cập nhật lịch sử.
    """
    requests = re.split(r'(?<=[.!?])\s+', request.strip())
    answer = ""
    context = ""
    for x in requests:
        res = ask(AskRequest(query=x))
        answer += res.answer + "\n"
        context += res.context + " "
    query_history.append((request, (answer, context)))
    return AskResponse(answer=answer, context=context)
