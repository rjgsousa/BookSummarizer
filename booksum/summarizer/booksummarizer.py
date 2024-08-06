import logging
import os

import yaml
from llama_index.core import Document, VectorStoreIndex, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

from booksum.utils.hash import get_file_hash
from booksum.utils.io_ops import load_parquet


class BookSummarizer(object):
    """Summarizer class

    A principled approach to summarize books.
    """

    def __init__(self,
                 logger,
                 root_path,
                 books_cfg_kb_filepath,
                 frac: float = 1):
        """
        Args:
            frac(float): loads a fraction of the knowledge base

        Returns:
            BookSumarizer cls

        """

        self.logger = logger
        self.data_path = os.path.join(root_path, "data/processed")
        if frac != 1:
            index_model_path = os.path.join(root_path, f"models/index_frac={frac}/")
        else:
            index_model_path = os.path.join(root_path, "models/index/")

        # ------------------------------------------------------------------------------------
        logger.info("Setting LLM ...")
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        self.llm = Groq(model="mixtral-8x7b-32768", api_key=GROQ_API_KEY, context_window=32768)

        # todo: replace this to SOTA sentence embedding
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="all-MiniLM-L6-v2",
            device="cuda"
        )

        if not os.path.exists(index_model_path):
            # ------------------------------------------------------------------------------------
            self.logger.warning("Loading book repository...")
            with open(os.path.join(root_path, books_cfg_kb_filepath), 'r') as file:
                self.books_cfg_kb = yaml.safe_load(file)

            books_hash = get_file_hash(str(self.books_cfg_kb))
            books = load_parquet(
                os.path.join(self.data_path, f"{books_hash}_clean.parquet")
            )

            books_from_booksum = load_parquet(
                os.path.join(self.data_path, "booksum.parquet")
            )
            # ------------------------------------------------------------------------------------
            self.logger.warning("Converting books (gutenberg) to LLamaIndex Document format...")
            documents = []

            if frac != 1:
                self.logger.warning("Setting a fraction of the entire dataset...")
                books = books.sample(frac=frac, random_state=65535)
                books_from_booksum = books_from_booksum.sample(frac=frac, random_state=65535)

            for index, record in books.iterrows():
                text = record['book-clean']
                title = record['title']
                documents.append(Document(text=text, doc_id=title))

            self.logger.warning("Converting books (booksum) to LLamaIndex Document format...")
            for index, record in books_from_booksum.iterrows():
                text = record['chapter']
                book_id = record['book_id']
                documents.append(Document(text=text, doc_id=book_id))

            self.logger.warning("Starting indexation ...")
            # indexation
            books_index = VectorStoreIndex.from_documents(documents, show_progress=False)
            books_index.storage_context.persist(persist_dir=index_model_path)
        else:
            self.logger.warning("Loading previous index ...")
            # rebuild storage context
            storage_context = StorageContext.from_defaults(persist_dir=index_model_path)
            # load index
            books_index = load_index_from_storage(storage_context)
            self.logger.warning("Loaded.")

        # init query engine
        self.books_engine = books_index.as_query_engine(similarity_top_k=3, llm=self.llm)

    def summarize_given_book_title(self, book_title: str) -> dict:
        """Summarizes an entire book

        Args:
            book_title (str): book title

        Returns:
            (base-response)
                base-response: the baseline response
        """
        prompt = (f"You are a summarizer specialist and domain expert. Given the book {book_title} "
                  f"provide me a clear summary without any prefix such as 'Here's the summary' or related.")

        return self._summarize(prompt)

    def summarize_given_text(self, text: str) -> dict:
        """Summarizes a given string

        Args:
            text (str): text

        Returns:
            (base-response)
                base-response: the baseline response
        """
        prompt = (f"You are a summarizer specialist and domain expert. Summarize the following text {text}. "
                  f"Provide me a clear summary without any prefix such as 'Here's the summary' or related.")

        return self._summarize(prompt)

    def _summarize(self, prompt):
        self.logger.warning(f"performing search to prompt: {prompt}")

        base_response = str(self.llm.complete(prompt))
        reasoning = str(self.books_engine.query(prompt))

        result = {
            'base-response': base_response,
            'simple-rag': reasoning
        }

        print(result)

        return result


if __name__ == "__main__":
    sum_logger = logging.getLogger()
    sum_logger.setLevel(logging.WARNING)
    console_handler = logging.StreamHandler()
    sum_logger.addHandler(console_handler)

    sum_logger.warning("Starting summarization... ")

    book_sum = BookSummarizer(
        sum_logger, root_path='../..',
        books_cfg_kb_filepath='config/books_to_process.yaml',
        frac=0.1
    )
    # summary = book_sum.summarize("Emma", "Jane Austen")
    summary = book_sum.summarize_given_book_title("The Last of the Mohicans")
    print(summary)
