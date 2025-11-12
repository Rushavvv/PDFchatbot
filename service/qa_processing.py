from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from service.pdf_processing import load_pdf_text
from langchain.schema import Document
from langchain.agents import create_tool_calling_agent, AgentExecutor

def get_conversational_chain(call_type, api_key):
    if call_type == "chat": 
        prompt_template = """
        Answer the question using the provided context. If the answer isn't found, say:
        "Answer is not available in the context." Don't give the wrong answer. At the end of every answer add  a line break and "-Rushav's pdfbot."

        If the question is not related to the context, politely respond that you are tuned to only answer questions related to the context.        
        
        Context:\n{context}\n
        Question:\n{question}\n

        Answer:
        """
        question_prompt = prompt_template
    
    elif call_type == "summary":
        prompt_template = """
        Summarize the following text in 5 bullet points:

        Context:\n{context}\n
        Summary:
        """
        question_prompt = prompt_template
    
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=question_prompt, input_variables=["context", "question"])

    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def answer_question_gemini(document_id, question, api_key):
    text = load_pdf_text(document_id)
    call_type = "chat"
    if not text:
        return None

    chain = get_conversational_chain(call_type, api_key)
    doc = Document(page_content=text)

    result = chain.invoke({"input_documents": [doc], "question": question})
    
    # If result is a dict, extract output_text
    if isinstance(result, dict) and "output_text" in result:
        return result["output_text"]
    elif isinstance(result, str):
        return result
    else:
        # fallback
        return str(result)


PDF_TEXT_DIR = "pdf_texts"
def summarize_pdf(document_id, api_key):
    text = load_pdf_text(document_id)
    call_type = "summary"
    if not text:
        return None

    chain = get_conversational_chain(call_type, api_key)
    doc = Document(page_content=text)

    result = chain.invoke({"input_documents": [doc]})
    
    # If result is a dict, extract output_text
    if isinstance(result, dict) and "output_text" in result:
        return result["output_text"]
    elif isinstance(result, str):
        return result
    else:
        # fallback
        return str(result)

