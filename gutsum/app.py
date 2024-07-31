## These are reference imports, please change with anything you want to use
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
import streamlit as st
from pathlib import Path


from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from controller.summary_generator import SummaryGeneratorController
from controller.gutenberg_text_splitter import split_recursively_books_to_chunks, create_document
from models.gutenberg_loader import GutenbergBooksLoader
from gutenberg_rag import get_llm

import os
 
    

    
    
    
## Function to get response from the model
def getAgentResponse(input_text, no_words, category):
    llm = CTransformers(model = '',
                        model_type = '',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01})
    
    ## PromptTemplate
    template = """Write a  {category} on {input_text} in less than {no_words} words"""

    prompt = PromptTemplate(input_variables = ["input_text", "no_words", "category"],
                            template = template)
    
    ## Generate the response
    response = llm(prompt.format(category=category,input_text=input_text,no_words=no_words))
    print(response)
    return response


if __name__ == "__main__":
    llm = get_llm()
    # Page title
    st.set_page_config(page_title='📝 Gutenberg Book Summarization App')
    st.title('📔📔📔 Gutenberg Book Summarization App')

    # Text input
    txt_input = st.text_area('Enter your chapter to summarize : ', '', height=400, max_chars= 10000)

    # User form
    result = []
    with st.form('summarize_form', clear_on_submit=True):
        submitted = st.form_submit_button('Submit')
        if submitted:
            tmp_txt = create_document(txt_input)
            print(tmp_txt)
            with st.spinner('Calculating...'):
                book_chunks = split_recursively_books_to_chunks([tmp_txt])
                print("********* book_chunks **********")
                print(book_chunks)
                response = SummaryGeneratorController.generate_summary_from_long_gutenberg_book(book_chunks, llm, verbose=True)
                result.append(response)

    if len(result):
        st.title('📝✅ Summarization Result')
        st.info(response)
    
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # book = GutenbergBooksLoader.load_unstructured_from_filesystem(f"{dir_path}/dataset/pg2274.txt")
    # print(book[:10])
    

    
    # book_chunks = split_recursively_books_to_chunks(book)
    # print(book_chunks[:3])
   
    
    
    # #### Testing the local LLM
    # llm = get_llm()
   
    # #### Summary
    # summary = SummaryGeneratorController.generate_summary_from_long_gutenberg_book(book_chunks[:3], llm)
    # print(summary)