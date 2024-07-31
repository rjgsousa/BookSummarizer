from langchain_community.document_loaders import GutenbergLoader
from langchain_community.document_loaders import UnstructuredFileLoader
import os

class GutenbergBooksLoader:
    """ Gutenberg book loader."""    
    @staticmethod
    def download_from_urls(book_urls: list = []):
        """
            Download a selection of books from the Project Gutenberg Catalog. 
        Args:
            book_urls (list, optional): list of links. Defaults to [].
        """
        all_books = []
        for index, book_url in enumerate(book_urls):
            loader = GutenbergLoader(book_url)
            data = loader.load()
            all_books.append(data)
        return all_books
    
    @staticmethod
    def load_from_filesystem(book_files : list = []):
        """Load book files from the local filesystem, thus a file is downloaded once and can be reused.
        Args:
            book_files (list, optional): book files. Defaults to [].

        Returns:
            _type_: raw text of the books
        """
        all_books = []
        for bfile in book_files:
            with open(bfile) as f:
                raw_books = f.read()
                all_books.append(raw_books)
        return all_books
    @staticmethod
    def load_unstructured_from_filesystem(book_file):
        """Load unstructured gutenberg book file from the local filesystem.
        Args:
            book_files (str): book file.

        Returns:
            _type_: document
        """
        loader = UnstructuredFileLoader(book_file, mode="elements")
        return loader.load()
