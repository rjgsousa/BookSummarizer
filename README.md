# A Platform for Books Processing and Summarization

This repository offers a ML solution for book summarization and an evaluation framework. To facilitate data and AI services, an API was developed with automated procedures to deploy the service. The provided data is served with [DVC](https://dvc.org/) for a faster reproducibility of the experiments here conducted. In cases where data is unavailable, concise instructions for obtaining it will be provided.

This project employs [Groq](https://groq.com/) as its Large Language Model (LLM) service, specifically utilizing the Llama (3.1) 70b model for its extensive context  window (128k tokens), accuracy, and strong performance. To use this LLM, you need to configure a token on the GroqCloud platform. While self-hosting LLMs via alternatives like vLLM or ollama is possible, this project does not currently encompass self-hosting options. This is an area we intend to address in the near future. Given the elevated context window of Llama 3.1, we truncated the `context_window` to a lower number to assess the Tree Summarizer performance.


### Installation
It is advisable to use a virtual environment (e.g., [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)) to manage the project dependencies.

Create a conda environment:
```bash
conda create -n book-summarization python=3.11
```

Activate the environment:
```bash
conda activate book-summarization
```

As it will be mentioned above, you need to have an environment variable named "GROQ_API_KEY" to leverage Groq. You should proceed as follows:

```bash
export GROQ_API_KEY=<YOUR-TOKEN>
```

Finally, you can now install the project:
```bash
make install
```

To run the service, simply type: 
```bash
make run
```

Please allow a few minutes for the system to download any missing data from the repository and load the index. The system will, by default, load the complete index, encompassing both [booksum](https://github.com/salesforce/booksum) and a selection of books from the Gutenberg Project catalog.

### ToDo

Dictionary Access:
- Current implementation directly accesses dictionary values/keys (by leveraging enumerators or other procedures for safer and more efficient access)

Containerization:
- Implement Docker to serve the system

Self-Hosted LLM:
- Explore using a self-hosted LLM, such as vLLM/ray or other alternatives

Logging:
- Introduce a logging mechanism to track system events and errors 

- System Efficiency:
Optimize the system to avoid calling the LLM to generate a baseline - simultaneously with the RAG approach (by improving efficiency by streamlining the LLM usage and reducing redundant calls)

RAG Index API:
- Restructure the API that serves the RAG index (by improving the API design to enhance usability, scalability, and maintainability)

Code Structure and Software Engineering Practices:
- Refactor the codebase to adhere to good software engineering practices  (suggestion: adopt Domain-Driven Design (DDD) principles, even if loosely, to improve code organization and maintainability)



### Documentation

For further assessments, check the documentation pages in [docs](docs).

### Author
- @rjgsousa