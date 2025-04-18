#pip install -qU langchain-google-genai
import warnings
warnings.filterwarnings("ignore") 

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain.chains import RetrievalQA


import getpass
import os
from dotenv import load_dotenv


load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")



loader = UnstructuredExcelLoader("resources\RAG_knowledge_base.xlsx", mode="elements")
docs = loader.load()

print(len(docs))


from langchain.text_splitter import RecursiveCharacterTextSplitter

# 2. Split Text into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
docs = text_splitter.split_documents(docs)



docs = filter_complex_metadata(docs)
# 3. Create Embeddings and Vector Store (Chroma)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") 
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index")





# 4. Define RetrievalQA Chain
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
)


from langchain_core.prompts import ChatPromptTemplate


# 5. Query the RAG System
query = "what is q2 loan data"
result = qa_chain.invoke(query)
print(result)