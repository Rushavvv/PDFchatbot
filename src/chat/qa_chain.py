from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

def get_conversational_chain(api_key):
    """Loading the question-answering chain for the chatbot."""
    prompt_template = """
    Your name is Apex, begin the first reply with "Hi! this is Apex your personal PDF chatbot" and add a line break.
    Answer the question using the provided context. If the answer isn't found, say:
    "Answer is not available in the context." dont give the wrong answer. At the end of every answer add "-Rushav's pdfbot."
    
    Context:\n{context}\n
    Question:\n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)
