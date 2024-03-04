"""
Script to interact with codellama from Hugging Face locally using LangChain.
"""

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate

MODEL_ID = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)


def model_pipeline(user_query: str) -> str:
    """
    Pipeline function that interacts with the model and prints streaming response.
    """
    pipe = pipeline("text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=1024,
                    repetition_penalty=1.1
    )
    hf = HuggingFacePipeline(pipeline=pipe)
    template = """<s>[INST] {user_query} [/INST]"""
    prompt = PromptTemplate.from_template(template)
    chain = prompt | hf
    result = chain.invoke({"user_query": user_query})
    print(type(result))
    print(result)
    return result