'''
Question answering from a given context.
'''

from transformers import pipeline

question_answerer = pipeline(task="question-answering", model="distilbert-base-cased-distilled-squad")
output = question_answerer(
    question="What work I do?",
    context="My name is Vineeth and I work as a Site Reliability Engineer at VMware in Bangalore, India",
)

print(output)
