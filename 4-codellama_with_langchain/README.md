## Overview
* In this exercise we will see how to work with codellama from Hugging Face locally using LangChain and Python.
* We will also enable streaming response from the LLM.

## Example

```
root@hf-3:/codellama# python3 new-codellama.py
Loading checkpoint shards: 100%|████████████████████████████████████████████████████████| 2/2 [00:03<00:00,  1.53s/it]

Ask codellama: given two unsorted integer lists. merge the two lists, sort the merged list, and find median using python. consider the length of the merged list while finding the median value.
Setting `pad_token_id` to `eos_token_id`:2 for open-end generation.
 Here is a possible solution to the problem:

def merge_and_find_median(list1, list2):
   # Merge the two lists
   merged_list = list1 + list2

   # Sort the merged list
   merged_list.sort()

   # Find the median value
   if len(merged_list) % 2 == 0:
       # Even number of elements in the merged list
       median = (merged_list[len(merged_list) // 2 - 1] + merged_list[len(merged_list) // 2]) / 2
   else:
       # Odd number of elements in the merged list
       median = merged_list[len(merged_list) // 2]

   return median

Explanation:

* First, we merge the two lists by concatenating them.
* Then, we sort the merged list using the `sort()` method.
* Next, we check whether the length of the merged list is even or odd. If it's even, we take the average of the middle two elements of the list. If it's odd, we simply take the middle element as the median.
* Finally, we return the median value.

Note that this solution assumes that both input lists are sorted in ascending order. If they are not sorted, you may need to add additional code to sort them before merging and finding the median.</s>

Ask codellama: /bye
root@hf-3:/codellama#

```

## References
* https://python.langchain.com/docs/integrations/llms/huggingface_pipelines
* [repetition_penalty](https://github.com/pinecone-io/examples/blob/master/learn/generation/llm-field-guide/llama-2/llama-2-70b-chat-agent.ipynb)
* [streaming response](https://github.com/langchain-ai/langchain/issues/2918)

