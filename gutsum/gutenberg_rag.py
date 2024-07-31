from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
import os
from controller.gutenberg_text_splitter import split_recursively_books_to_chunks
from models.gutenberg_loader import GutenbergBooksLoader


@staticmethod 
def create_faiss_vector_store(book_chunks, embedding, cache = True):
    """Creates a vector store from the provided book chunks, 
       it uses the provided embedding model to create vectors.
       The same embedding model must be keep

    Args:
        book_chunks (Document): collection of chunks
        embedding (Object): Embedding model
        cache (boolean): Select to cache or not the generated store
    """
    vectorstore = FAISS.from_documents(book_chunks,
                                       embedding)
    if cache:
        vectorstore.save_local("faiss_vector_store")
        
    return vectorstore


    
@staticmethod
def get_embedding_model(name = "BAAI/bge-large-en-v1.5"):
    """ Get an embedding model based on the provided name.
    Args:
        name (str, optional): selector. Defaults to "".

    Returns:
        _type_: Embedding model
    """
    # Todo: this function can implement different type of embedding such as OpenAi and other models...
    return HuggingFaceEmbeddings(
        model_name=name,    
    )

@staticmethod 
def get_llm(name = "tinyllama", temperature=0.01, num_predict = 1000): 
    """ Return the LLM to be used for RAG
    Args:
        name (str, optional): the name of the llm model.

    Returns:
        _type_: LLM Object
    """
    # for the testing purpose, tinyllama was used instead of Llama3 or 2 as it does not require a lot of computing power.
    llm = Ollama(model=name, temperature=temperature, num_predict=num_predict) 
    return llm


@staticmethod  
def load_faiss_vector_store(name, embedding):
    """Load a vector store

    Args:
        name (str, optional): Defaults to "faiss_vector_store".

    Returns:
        _type_: VectorStore
    """
    ## >>> Warning 
    ## allow_dangerous_deserialization=False, prevents any dangerous executions 
    ## by default from a .pkl file
    ## Only for testing purpose, it was made True. 
    return FAISS.load_local(name, embedding, allow_dangerous_deserialization=True)
    
    

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ### load books
    book = GutenbergBooksLoader.load_unstructured_from_filesystem(f"{dir_path}/dataset/pg2274.txt")
    print(book[:10])
    ### Split 
    book_chunks = split_recursively_books_to_chunks(book)
    print(book_chunks[:3])
    
    ### Embeddings
    embedding = get_embedding_model()
    print(embedding)
    
    ### VectorStore 
    ## Uncomment the below code to generate or update the vector store 
    #vector_store = create_faiss_vector_store(book_chunks, embedding)
    ## >>> Warning 
    ## allow_dangerous_deserialization=False, prevents any dangerous executions by default from a .pkl file
    ## Only for testing purpose, it was made True. 
    vectorstore = FAISS.load_local("faiss_vector_store", embedding, allow_dangerous_deserialization=True) 
    
    #### Retriever 
    retriever = vectorstore.as_retriever(search_kwargs={"k" : 5, 'score_threshold': 0.8})
    relevant_docs = retriever.get_relevant_documents("how to control the mind")
    print(relevant_docs)