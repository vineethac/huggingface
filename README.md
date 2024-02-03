## Overview
This repository serves as a guide to help you get started with Hugging Face, including:

* Downloading and utilizing Hugging Face models locally via the Python Transformers library.
* Constructing an API for your LLM application using FastAPI.
* Containerizing your project with Docker.
* Deploying and running your containerized application on a Kubernetes cluster.

## Hugging Face
* Major hub for open-source machine learning (ML) models.
* There are hundreds of pre-trained LLMs available on Hugging Face.
* Hugging Face (HF) also has several data sets that can be used to fine tune or train LLMs.
* Hugging Spaces used to build and deploy ML models/ apps.
* Models can be found at: huggingface.co/models
* Hugging Face Hub: To make use of models hosted in HF. You will need an access token to use it.

## Language models
#### Text-to-Text Generation (sequence to sequence) Models

* Encoder - Decoder model
* Text-to-text generation is frequently employed for tasks such as translating English sentences into French or summarizing lengthy paragraphs.
* Examples of Text Generation models include T5 and BART, which are commonly used in question-answering, Translation, and Summarization tasks.


#### Text Generation (Casual LM) Models

* Decoder only model. 
* Often employed for tasks such as sentence completion and generating the next lines of poetry when given a few lines as input.
* Examples of Text Generation models include the GPT family, BLOOM, and PaLM, which find applications in Chatbots, Text Completion, and content generation.


## Transformers library 
* Python library developed by HF that makes downloading and training ML models easy.
* You can filter models that can be used with the Transformers library.
* Not all models can be used with the Transformers library.
* Pipeline function from the Transformers library can be used to interact with the LMs.
* If you don’t provide a model name, during runtime it will automatically find a default model and download it from HF.
* Second time onwards, it will use the cached copy of the model when prompted.
* Some of the currently available pipelines are:

    - feature-extraction (get the vector representation of a text)
    - Fill-mask
    - ner (named entity recognition)
    - Question-answering
    - Sentiment-analysis
    - Summarization
    - Text-generation
    - Translation
    - Zero-shot-classification

* Pretrained models are downloaded and locally cached at: ~/.cache/huggingface/hub/



