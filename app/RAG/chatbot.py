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



def get_answer(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") 
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    retriever = new_db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
    )
    result =  qa_chain.invoke(user_question)
    return result['result']




    #sample useage
    user_question = input("Enter your question: ")
    answer = get_answer(user_question)
    print(answer)