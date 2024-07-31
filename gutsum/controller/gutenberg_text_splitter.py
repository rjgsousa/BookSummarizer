from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


@staticmethod
def create_document(text : str):
    """Simplify the document creation from a user input

    Args:
        text (str): the provided text

    Returns:
        _type_: Document
    """
    return Document(page_content=text, metadata={"source": "local"})
    #return Document(page_content=text, metadata={"source": "user_input"})

@staticmethod
def split_recursively_books_to_chunks(books, chunk_size = 512, chunk_overlap=20):
    """Split the books into smaller chunks
    Args:
        books (list): collection of books
        chunk_size (int, optional): preferred chunk size. Defaults to 512.
    """
    text_splitter = RecursiveCharacterTextSplitter(
                                                   chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap, 
                                                   length_function=len,
                                                   #separators= ["\n\n", "***\n\n\n\n\n", "\n\n\n\n\" ],
                                                   is_separator_regex=False)
    
    chunked_books = text_splitter.split_documents( books )
    return chunked_books
