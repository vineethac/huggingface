from transformers import pipeline

unmasker = pipeline(task="fill-mask", model="distilroberta-base")
output = unmasker("This course will teach you all about <mask> models.", top_k=5)

for item in output:
    print(item)
