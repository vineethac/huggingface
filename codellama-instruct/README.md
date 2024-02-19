## Overview
* In this exercise we will see how to interact with CodeLlama - Instruct model from Hugging Face locally using the transformers library and Python.
* Here I am using the 7 billion parameters model. 
* Size of this model is around 13.5G.
* I am using Python 3.10.12.

## Example
```
root@hf-5:/#
root@hf-5:/# python3 codellama_prompt.py
tokenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 749/749 [00:00<00:00, 3.44MB/s]
tokenizer.model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 500k/500k [00:00<00:00, 4.12MB/s]
tokenizer.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.84M/1.84M [00:00<00:00, 9.76MB/s]
special_tokens_map.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 411/411 [00:00<00:00, 2.08MB/s]
config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 646/646 [00:00<00:00, 3.51MB/s]
model.safetensors.index.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 25.1k/25.1k [00:00<00:00, 47.9MB/s]
model-00001-of-00002.safetensors: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 9.98G/9.98G [02:02<00:00, 81.2MB/s]
model-00002-of-00002.safetensors: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3.50G/3.50G [00:45<00:00, 76.7MB/s]
Downloading shards: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [02:48<00:00, 84.38s/it]
Loading checkpoint shards: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:20<00:00, 10.10s/it]
generation_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 116/116 [00:00<00:00, 444kB/s]


Ask codellama/CodeLlama-7b-Instruct-hf: reverse a list in python.
Setting `pad_token_id` to `eos_token_id`:2 for open-end generation.
Result: <s>[INST] reverse a list in python. [/INST]  There are several ways to reverse a list in Python. Here are a few methods:

1. Using the `reversed()` function:

my_list = [1, 2, 3, 4, 5]
reversed_list = list(reversed(my_list))
print(reversed_list)  # [5, 4, 3, 2, 1]

2. Using slicing:

my_list = [1, 2, 3, 4, 5]
reversed_list = my_list[::-1]
print(reversed_list)  # [5, 4, 3, 2, 1]

3. Using the `reverse()` method:

my_list = [1, 2, 3, 4, 5]
my_list.reverse()
print(my_list)  # [5, 4, 3, 2, 1]

Note that the `reverse()` method reverses the list in place, meaning that it modifies the original list. The other two methods create a new list with the elements in reverse order.



Ask codellama/CodeLlama-7b-Instruct-hf: Provide examples of working with dict in Python.
Setting `pad_token_id` to `eos_token_id`:2 for open-end generation.
Result: <s>[INST] Provide examples of working with dict in Python. [/INST]  Sure, here are some examples of working with dictionaries in Python:

1. Creating a dictionary:

my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}

2. Accessing values in a dictionary:

print(my_dict['name'])  # Output: John
print(my_dict['age'])   # Output: 30
print(my_dict['city'])  # Output: New York

3. Modifying a dictionary:

my_dict['name'] = 'Jane'
my_dict['age'] = 31
my_dict['city'] = 'Los Angeles'

4. Adding new key-value pairs to a dictionary:

my_dict['country'] = 'USA'
my_dict['state'] = 'California'

5. Deleting key-value pairs from a dictionary:

del my_dict['name']
del my_dict['age']

6. Checking if a key is in a dictionary:

if 'name' in my_dict:
    print('The "name" key is in the dictionary.')

7. Looping through a dictionary:

for key, value in my_dict.items():
    print(f'{key}: {value}')

8. Using dictionary methods:

my_dict.keys()  # Returns a list of all keys in the dictionary
my_dict.values()  # Returns a list of all values in the dictionary
my_dict.items()  # Returns a list of all key-value pairs in the dictionary
my_dict.get('name')  # Returns the value for the 'name' key, or None if the key is not found
my_dict.setdefault('name', 'John')  # Sets the value for the 'name' key to 'John' if it is not already set
my_dict.pop('name')  # Removes the 'name' key and returns its value

These are just a few examples of what you can do with dictionaries in Python. There are many more methods and features available, so be sure to check out the official Python documentation for more information.



Ask codellama/CodeLlama-7b-Instruct-hf: /bye
root@hf-5:/#

```

## References
* https://ai.meta.com/blog/code-llama-large-language-model-coding/
* https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf
* https://huggingface.co/blog/codellama

