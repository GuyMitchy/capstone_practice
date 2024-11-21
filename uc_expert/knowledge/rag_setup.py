from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

class UCExpertRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()  # Changed from OllamaEmbeddings
        self.vector_store = None
        self.qa_chain = None
        
    def initialize_knowledge_base(self):
        loader = DirectoryLoader('knowledge/docs/', glob="*.md")
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory="knowledge/db"
        )
        
        llm = ChatOpenAI(model="gpt-4")  # Changed from Ollama
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )
        
    def get_response(self, question, context=""):
        if not self.qa_chain:
            self.initialize_knowledge_base()
            
        prompt = f"""
        Context: {context}
        Question: {question}
        Please provide accurate medical information based on the context and question.
        """
        return self.qa_chain.run(prompt)