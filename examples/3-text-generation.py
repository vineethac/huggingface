from transformers import pipeline

generator = pipeline(task="text-generation", model="gpt2")
output = generator("In this course, we will teach you how to", max_length=30, num_return_sequences=5)

for item in output:
    print(item)
