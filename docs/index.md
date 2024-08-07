# A System for Books Processing and Summarization

This repository offers a ML solution for book summarization and an evaluation framework. To facilitate data and AI services, an API was developed with automated procedures to deploy the service. The provided data is served with [DVC](https://dvc.org/) for a faster reproducibility of the experiments here conducted. In cases where data is unavailable, concise instructions for obtaining it will be provided.

This project employs [Groq](https://groq.com/) as its Large Language Model (LLM) service, specifically utilizing the Llama (3.1) 70b model for its extensive context  window (128k tokens), accuracy, and strong performance. To use this LLM, you need to configure a token on the [GroqCloud](https://console.groq.com/) platform. While self-hosting LLMs via alternatives like vLLM or ollama is possible, this project does not currently encompass self-hosting options. This is an area we intend to address in the near future. Given the elevated context window of Llama 3.1, we truncated the context_window to assess the Tree Summarizer performance.

## Improvements

To enhance the reproducibility, efficiency, and overall quality of the system, the following improvements are proposed:

First and foremost, we recommend refactoring the codebase to replace direct access to dictionary values/keys with safer and more efficient methods, such as enumerators. This improvement will not only promote better code readability and maintainability but also reduce the risk of errors related to dictionary access.

To streamline deployment and ensure reproducibility across different environments, I suggest implementing Docker/PodMan. Containerization guarantees consistent behavior and dependencies, making it simpler to set up and run the system on various platforms.

Exploring the feasibility of integrating a self-hosted LLM, leveraging vLLM/ray or other suitable alternatives, into the system is another key improvement. By hosting the LLM locally, we will reduce reliance on external services, and potentially improve performance.

To enhance observability and gain deeper insights into the system's behavior, we propose augment existing logging framework. By capturing system events, errors, and relevant information during runtime, this framework will empower developers to effectively monitor, debug, and troubleshoot the system. The increased observability will enable faster issue resolution, proactive identification of potential problems, and continuous optimization of the system's performance. Moreover, the logging framework will provide valuable data for analysis, allowing for data-driven decision-making and facilitating the identification of improvement opportunities. By prioritizing observability through robust logging, the system will become more transparent, maintainable, and resilient.

Efficiency is crucial, and we recommend analyzing and optimizing the system's performance by:

1. Identifying and eliminating redundant LLM calls, such as generating a baseline simultaneously with the RAG approach.
2. Streamlining the LLM usage to minimize unnecessary computations and improve overall system performance.
3. To enhance the usability, scalability, and maintainability of the RAG index API, we suggest restructuring it. Consider implementing REST principles, proper error handling, and clear documentation to facilitate seamless integration and usage of the API.

Lastly, we strongly advocate for the adoption of software engineering best practices. This involves:

1. Refactoring the codebase to promote modularity, reusability, and testability.
2. Apply paradigms such as Domain-Driven Design (DDD) principles, even if loosely, to improve code organization, separation of concerns, and alignment with business requirements.
3. Implementing unit testing, integration testing, and continuous integration/continuous deployment (CI/CD) practices to ensure code quality and reliability.

# Methods


## Topic Modeling
The first task in the project involved downloading a curated selection of books from the Project Gutenberg Catalog. To streamline the data management and ingestion process, the `gutenbergpy` package was utilized along with a configuration file available in the [config](../config/books_to_process.yaml) directory.

In terms of pre-processing, the approach taken in this project leveraged the power of transformers, which come equipped with their own tokenizers. As a result, minimal pre-processing was required, with only minor text clean-up procedures applied to ensure the data was in a suitable format for the transformer models. However, it is worth noting that if one wishes to employ previous methodologies for pre-processing, the necessary code and resources can be found in the [booksum/topic_modeling](../booksum/topic_modeling) directory.

To further enhance the understanding of the downloaded dataset, topic modeling was performed using the [BERTopic](https://maartengr.github.io/BERTopic/index.html) library. This additional step aimed to uncover the underlying themes and topics present in the selected books.

To present the findings of the topic modeling analysis, a dedicated notebook was created. This notebook provides a comprehensive visualization of the results, allowing for easy exploration and interpretation of the discovered topics. 

## Book Summary Generation

For the second task, I leveraged the powerful Llama (3.1) 70b model, which boasts an extensive context window of 128k tokens. This expansive context window was efficiently utilized by the LLM serving infrastructure provided by [Groq](https://groq.com/). To further enhance the capabilities of the chosen LLM, I integrated the [llamaindex](https://www.llamaindex.ai/) library. The llamaindex library was selected for its ability to efficiently index and retrieve relevant information from large text corpora, making it an ideal choice for the retrieval augmented generation (RAG) pipeline. Given the elevated context window of Llama 3.1, we truncated the `context_window` to a lower number to assess the Tree Summarizer performance.

To enable the RAG capabilities, I used a diverse collection of books: the Gutenberg Catalogue, which offers a wide range of public domain books, and the [Booksum](https://github.com/salesforce/booksum) dataset, which includes a subset of the Gutenberg books. The NLTK package also provided a small subset of books of this catalogue, but it was not used.

To achieve the additional bonus objective of improving performance, I included some literary analysis articles. These articles provide valuable insights and contextual information that can enhance the quality and depth of the generated book summaries.

To streamline the experimentation process and improve iteration velocity, I implemented some caching strategies. This caching mechanism allowed me for efficient storage and retrieval of previously generated results, reducing redundant computations and enabling faster experimentation cycles.
