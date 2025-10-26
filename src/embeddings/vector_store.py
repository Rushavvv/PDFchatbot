from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def get_text_chunks(text):
    """Spliting text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=100)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    """Generatung embeddings and saving the FAISS index."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("data/vectorstores/faiss_index")
    return vector_store
