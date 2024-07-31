from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain

class SummaryGeneratorController:
    """A class helper for generating summary from books."""
    
    
    @staticmethod
    def generate_custom_summary_from_long_gutenberg_book(books, llm, token_max = 1000):
        """ Return a custom summary for a given book
        Args:
            books (List): Documents.
            llm (Object): The selected LLM
            token_max (int): maximum tokens
        Returns:
            _type_: LLM Object
        """
        #>> Step 1
        # Map
        map_template = """The following is a set of documents
        {books}
        Based on this list of docs, please identify the main themes 
        Helpful Answer:"""
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)
        
        #>> Step 2
        # Reduce
        reduce_template = """The following is set of summaries:
        {books}
        Take these and distill it into a final, consolidated summary of the main themes. 
        Helpful Answer:"""
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)
        
        #>> Step 3
        # Combining results
        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="books"
        )    
        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            collapse_documents_chain=combine_documents_chain,
            token_max=token_max,
        )
        #>> Step 4 run MapReduce
        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            reduce_documents_chain=reduce_documents_chain,
            document_variable_name="books",
            return_intermediate_steps=True,
        )
        return map_reduce_chain.invoke(books)

    @staticmethod
    def generate_summary_from_long_gutenberg_book(book_chunks, llm, token_max = 1000, verbose = False):
        """Generate a summary of the given chunks
        Args:
            book_chunks (Document): book chunks
            llm (_type_): LLM
            token_max (int, optional): Maximum number of tokens. Defaults to 1000.
        Returns:
            _type_: List
        """
        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            verbose=verbose,
            token_max=token_max
        )
        return summary_chain.run(book_chunks)
    
    @staticmethod
    def generate_refined_summary_from_long_gutenberg_book(book_chunks, llm, token_max = 1000, verbose = False):
        """Generate a summary of the given chunks, using the refine approach.
        Args:
            book_chunks (Document): book chunks
            llm (_type_): LLM
            token_max (int, optional): Maximum number of tokens. Defaults to 1000.
        Returns:
            _type_: List
        """
        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type="refine",
            verbose=verbose
        )
        return summary_chain.run(book_chunks)