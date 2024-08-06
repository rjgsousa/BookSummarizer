import requests
import streamlit as st

_api_url = "http://localhost:8001/summarize/"


def book_summary_api(api_url, data=None):
    # make request
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None


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
            results = book_summary_api(_api_url, {"book": query})

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
