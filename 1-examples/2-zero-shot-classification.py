from transformers import pipeline

classifier = pipeline(task="zero-shot-classification", model="facebook/bart-large-mnli")
output = classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)

print(output)
