from langchain_community.document_loaders import UnstructuredExcelLoader


#loading excel file
loader = UnstructuredExcelLoader("resources\unprotected.xlsx", mode="elements")
docs = loader.load()




from langchain.text_splitter import RecursiveCharacterTextSplitter

# 2. Split Text into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
docs = text_splitter.split_documents(docs)



