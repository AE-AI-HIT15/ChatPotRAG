# ask.py
import re
from src.config import query_history
from src.models import AskRequest, AskResponse
from src.RAG import retrieve, generate_answer

def ask(request: AskRequest) -> AskResponse:
    """
    Process a single question:
        - Record the question in the history.  
        - Retrieve the related documents (k=3 and k=1).  
        - If no data is found, return an error message.  
        - Otherwise, combine the context and call the function to generate an answer.
    """
    query = request.query
    query_history.append(query)
    
    retrieved_list = retrieve(query, k=3)
    query_fake_list = retrieve(query, k=1)
 
    if not retrieved_list:
        return AskResponse(answer="Sorry, I don't have enough information to answer this question: " + query, context="")
    
    context = " ".join(retrieved_list)
    query_fake = query_fake_list[0] if query_fake_list else query
    answer = generate_answer(query_fake, context)
    return AskResponse(answer=answer, context=context)
    
def ask_endpoint(request: str) -> AskResponse:
    """
    Process a string of multiple questions:
        - Split the string into individual sentences based on periods, question marks, and exclamation marks.  
        - For each sentence, call the `ask` function to get the answer.  
        - Concatenate the results of all sentences and update the history.
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
