from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from service.pdf_processing import load_pdf_text
from langchain.schema import Document
from langchain.agents import create_tool_calling_agent, AgentExecutor

def get_conversational_chain(api_key):
    prompt_template = """
    Your name is Apex, begin the first reply with "Hi! this is Apex your personal PDF chatbot" and add a line break.
    Answer the question using the provided context. If the answer isn't found, say:
    "Answer is not available in the context." Don't give the wrong answer. At the end of every answer add  a line break and "-Rushav's pdfbot."

    If the question is not related to the context, politely respond that you are tuned to only answer questions related to the context.
    Also if the question is ambigious such as "what", "huh", etc just answer with "Please provide a more specific question related to the context."
    
    
    Context:\n{context}\n
    Question:\n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def answer_question_gemini(document_id, question, api_key):
    text = load_pdf_text(document_id)
    if not text:
        return None

    chain = get_conversational_chain(api_key)
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

