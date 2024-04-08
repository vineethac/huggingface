"""
Script to interact with codellama from Hugging Face locally using LangChain.
"""

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, pipeline
from langchain.prompts import PromptTemplate

MODEL_ID = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
streamer = TextStreamer(tokenizer, skip_prompt=True)

def user_prompt() -> str:
    """
    Get user input.
    """
    user_query = input("Ask codellama: ")
    return user_query


def model_pipeline(user_query: str) -> None:
    """
    Pipeline function that interacts with the model and prints streaming response.
    """
    pipe = pipeline("text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    streamer=streamer,
                    max_new_tokens=1024,
                    repetition_penalty=1.1
    )
    hf = HuggingFacePipeline(pipeline=pipe)
    template = """<s>[INST] {user_query} [/INST]"""
    prompt = PromptTemplate.from_template(template)
    chain = prompt | hf
    chain.invoke({"user_query": user_query})


def main():
    """
    Main function gets user input and calls model_pipeline.
    """
    while True:
        user_query = user_prompt()
        if user_query == "/bye":
            break
        model_pipeline(user_query)


if __name__ == "__main__":
    main()
