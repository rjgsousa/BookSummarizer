import streamlit as st

from booksum.utils.service_utils import book_summary_api

def main():

    # title for the webpage
    st.title("Book Summarizer")

    options = st.selectbox(
        'What would be the retrieval augmented approach?',
        ['LLM', 'LLM+RAG'],
        index=None,
        placeholder="Select summarization method...",
    )

    query = st.text_input("What is the book that you would like to be summarized:")

    if st.button("Summarize"):
        if query:
            results = book_summary_api({"book": query}, given='book-title')

            # which result will be displayed to the end user
            if options == 'LLM':
                results = results['base-response']
            elif options == 'LLM+RAG':
                results = results['simple-rag']
            else:
                # invalid option for some unknown reason
                results = results['base-response']

            st.write(f"Results for: {query}")
            st.write(results)
        else:
            st.write("Please enter a query to search.")


if __name__ == "__main__":
    main()
