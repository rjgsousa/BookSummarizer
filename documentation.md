
# Solution
This implementation provides a Poof-of-Concept of the Gutenburg book summarization, using python, HuggingFace, TinyLlama and Langchain. To meet the requirement needs, the implementation was coded across different files and comprises different steps.
## User Interface
Additionally, an User Interface (UI) was developed using Streamlit library to experiment with the book summarization feature, Figure 1-2.
Figure 1
![app](./img/image2.png)
Figure 2
![app](./img/image1.png)

## Install 
Navigate to the root directory, open the terminal and run the following command line.
```
pip install -r requirements.txt
```

## Run
```
streamlit run app.py

```

## Data Collection
The logic behind Downloading and processing Gutenberg books is implemented in the python file:```models/gutenberg_loader.py```, which is a factory class that provides the required methods.

## Build a RAG pipeline and augment the chosen LLM to produce book summaries
### LLM
In this implementation, I used [TinyLlama](https://github.com/jzhang38/TinyLlama), which is a 1.1 Billion LLM (a Llama model pre-trained on 3 trillion tokens), optimized to run on consumer hardware (laptop, phone...). 

The TinyLlama LLM is served via [Ollama](https://ollama.com), which provides a convenient way to access and interact with the LLM locally without relying on remote servers or cloud-based solutions, especially during the development process. It is also Compatible with OpenAI API, which makes it easy to switch between different LLMs.
 
**Install** 
```
curl -fsSL https://ollama.com/install.sh | sh
```

**Serve**
```
ollama run tinyllama

```
### RAG

The RAG pipeline was implemented using [Langchain](https://www.langchain.com/) libraries. It was implemented in the python files:
```
gutenberg_rag.py
rag_app.ipynb 
```
It requires jupyter notebook extension to be installed, if you are using [VSCode IDE](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
#### RAG-Pipline

In general in comprises the following steps:

- Loading the books with the help of GutenbergBooksLoader.
- Chunking them to fit in the LLM context length.
- Get the embedding model.
- Build a vector store for the vectors.
- Query the Vector Store and get the relevant documents, which are handed to the LLM.

### Summarization 
To overcome the challenges of the requirements, a sophisticated approach was developed using MapReduce algorithm it can be found in the python file ```controller/summary_generator.py```.   



### Evaluation 
The details of the implemetation for the evaluation can be found in the file ```booksum_evaluation.ipynb```

A number of challenged were faced. Especially, for aligning the dataset [kmfoda/booksum](https://huggingface.co/datasets/kmfoda/booksum) with the summarization.

The [kmfoda/booksum](https://huggingface.co/datasets/kmfoda/booksum) dataset, may provide for each book's title, a single or multiple summaries for each chapters. Thus, the downloaded books required to be parsed and chunked by chapters.

![app](./img/image_eval.png)