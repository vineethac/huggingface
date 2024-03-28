"""
Script to interact with LLM from Hugging Face locally using LangChain.
"""

import logging
import coloredlogs
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate


coloredlogs.install()

# Setting log level
logging.basicConfig(level="INFO")

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)


def model_pipeline(user_query: str) -> str:
    """
    Pipeline function that interacts with the model and returns response.
    """
    logging.info(f"Model: {MODEL_ID}")
    pipe = pipeline("text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=10240,
                    repetition_penalty=1.1
    )
    hf = HuggingFacePipeline(pipeline=pipe)
    template = """<s>[INST] {user_query} [/INST]"""
    prompt = PromptTemplate.from_template(template)
    chain = prompt | hf
    result = chain.invoke({"user_query": user_query})

    # Remove the prompt template from the result
    result = result.replace(f"<s>[INST] {user_query} [/INST]", "")
    logging.info(f"LLM response: {result}")
    return result
