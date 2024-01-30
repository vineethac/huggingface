from transformers import pipeline

ner = pipeline(task="ner", grouped_entities=True, model="dbmdz/bert-large-cased-finetuned-conll03-english")
output = ner("My name is Vineeth A C and I work at VMware in Bangalore, India.")

for item in output:
    print(item)
