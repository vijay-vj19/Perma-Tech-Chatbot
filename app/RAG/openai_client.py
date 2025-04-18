import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
import getpass

# Load environment variables
load_dotenv()

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

from langchain_community.chat_models import ChatOpenAI

# Load and preprocess the Excel document
excel_path = "resources/Preprocessed.xlsx"
if not os.path.exists(excel_path):
    raise FileNotFoundError(f"File not found: {excel_path}")

loader = UnstructuredExcelLoader(excel_path, mode="elements")
docs = loader.load()

if not docs:
    raise ValueError("No documents found in the Excel file.")

print(f"Loaded {len(docs)} documents.")

# Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(docs)

# Create vector store with OpenAI embeddings
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)
vectorstore.persist()

# Initialize the language model
llm = ChatOpenAI(model_name="gpt-3.5-turbo")  # Change to gpt-4 if needed
retriever = vectorstore.as_retriever()

# Setup RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
)

# Run query
query = "What are the different client data in the dataset?"
result = qa_chain.invoke(query)
print("Answer:", result["result"] if "result" in result else result)
