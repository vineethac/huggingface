"""
Sample code snipet that shows how to interact with codellama model locally 
using the transformers library.
"""

from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLMInteraction:
    """
    Class and methods for interacting with the LLM and prints response.
    """
    def __init__(self, model_name, code_generator):
        self.model_name = model_name
        self.code_generator = code_generator


    def print_llm_response(self, generated_code):
        """
        Prints response from the LLM.
        """
        for item in generated_code:
            print(f"Result: {item['generated_text']}")
        print("\n \n")

    def query_llm(self, prompt):
        """
        Query the LLM with user prompt template.
        """
        generated_code = self.code_generator(prompt, max_new_tokens=50000)
        return generated_code


    def user_prompt(self):
        """
        Get user input and create the prompt template.
        """
        # Generate code for an input string
        input_string = input(f"Ask {self.model_name}: ")
        prompt = f"<s>[INST] {input_string.strip()} [/INST]"
        return prompt


def load_model(model_name):
    """
    Download/ load the model locally.
    """
    tokenizer = AutoTokenizer.from_pretrained(f"{model_name}")
    model = AutoModelForCausalLM.from_pretrained(f"{model_name}")

    # Create a pipeline
    code_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    return code_generator


def main():
    """
    Main function.
    """
    model_name = "codellama/CodeLlama-7b-Instruct-hf"
    code_generator = load_model(model_name)
    interact = LLMInteraction(model_name, code_generator)

    while True:
        prompt = interact.user_prompt()
        if prompt == "<s>[INST] /bye [/INST]":
            break
        generated_code = interact.query_llm(prompt)
        interact.print_llm_response(generated_code)


if __name__ == "__main__":
    main()
