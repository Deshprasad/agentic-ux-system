from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

def load_kb(file_path):
    loader = TextLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(chunks,
                                         embedding=None,
                                           persist_directory="data/vector"
                                           )
    return vectorstore
def query_kb(vectorstore, query):
    results = vectorstore.similarity_search(query)
    return results

if __name__ == "__main__":
    vs = load_kb("data/documents/ux_notes.txt")
    results = query_kb(vs, "What is UX?")
    print(results)