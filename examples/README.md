## Access to a Kubernetes cluster
* For the purpose of testing I am going to run these examples in a basic Python pod deployed on Kubernetes.
* The debug image that I am using already has Python and some other utilities pre installed.
* Instead of directly testing it on my Mac, I prefer testing them in a K8s pod!

```
❯ KUBECONFIG=gckubeconfig kg no
NAME                                             STATUS   ROLES                  AGE   VERSION
tkc01-control-plane-49jx4                        Ready    control-plane,master   19d   v1.23.8+vmware.3
tkc01-control-plane-m8wmt                        Ready    control-plane,master   27d   v1.23.8+vmware.3
tkc01-control-plane-z6gxx                        Ready    control-plane,master   19d   v1.23.8+vmware.3
tkc01-worker-nodepool-a1-pqq7j-fd5784bcc-9r6t5   Ready    <none>                 27d   v1.23.8+vmware.3
tkc01-worker-nodepool-a1-pqq7j-fd5784bcc-cxmwm   Ready    <none>                 19d   v1.23.8+vmware.3
tkc01-worker-nodepool-a1-pqq7j-fd5784bcc-mszdm   Ready    <none>                 27d   v1.23.8+vmware.3

❯ KUBECONFIG=gckubeconfig k run hf-2 --image=vineethac/debug -- sleep infinity

❯ KUBECONFIG=gckubeconfig kg po hf-2
NAME   READY   STATUS    RESTARTS   AGE
hf-2   1/1     Running   0          27h
```

## Exec into the Python pod 
* Create the required Python files or copy them using `kubectl cp` command.

```
❯ KUBECONFIG=gckubeconfig k exec -it hf-2 -- bash
root@hf-2:/#
root@hf-2:/# cd transformers-course/
root@hf-2:/transformers-course#
root@hf-2:/transformers-course# ls
1-sentiment-analysis.py  2-zero-shot-classification.py  3-text-generation.py  4-fill-mask.py  5-named-entity-recognition.py  6-question-answering.py  7-summarization.py  8-translation.py
root@hf-2:/transformers-course#
```

## Install requirements
* Exec into the pod and then pip install required packages.

```
root@hf-2:/transformers-course#
root@hf-2:/transformers-course# pip install "transformers[sentencepiece]" torch
```

## Running the language models from Hugging Face
* Note that if the models are not already present on your local machine, it will first download the required components and then use it.
* In my case, these models are already present in the cache as I've ran these examples earlier.
* You can find them at: `~/.cache/huggingface/hub/`

```
root@hf-2:/transformers-course# cd ~/.cache/huggingface/hub/
root@hf-2:~/.cache/huggingface/hub#
root@hf-2:~/.cache/huggingface/hub# ls
models--Helsinki-NLP--opus-mt-fr-en                        models--distilbert-base-cased-distilled-squad            models--distilroberta-base         models--gpt2                            version.txt
models--dbmdz--bert-large-cased-finetuned-conll03-english  models--distilbert-base-uncased-finetuned-sst-2-english  models--facebook--bart-large-mnli  models--sshleifer--distilbart-cnn-12-6
root@hf-2:~/.cache/huggingface/hub#
```

### sentiment-analysis

```
root@hf-2:/transformers-course# python3 1-sentiment-analysis.py
[{'label': 'POSITIVE', 'score': 0.9598046541213989}, {'label': 'NEGATIVE', 'score': 0.9994558691978455}]
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

### zero-shot-classification

```
root@hf-2:/transformers-course# python3 2-zero-shot-classification.py
{'sequence': 'This is a course about the Transformers library', 'labels': ['education', 'business', 'politics'], 'scores': [0.8445965647697449, 0.11197595298290253, 0.0434274896979332]}
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

### text-generation

```
root@hf-2:/transformers-course# python3 3-text-generation.py
Truncation was not explicitly activated but `max_length` is provided a specific value, please use `truncation=True` to explicitly truncate examples to max length. Defaulting to 'longest_first' truncation strategy. If you encode pairs of sequences (GLUE-style) with the tokenizer you can select this strategy more precisely by providing a specific strategy to `truncation`.
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
{'generated_text': 'In this course, we will teach you how to build real tools for real business development and to quickly identify new ways that you may create content that you'}
{'generated_text': 'In this course, we will teach you how to identify and apply an online survey tool to evaluate potential students who are eligible for a job posting or job'}
{'generated_text': 'In this course, we will teach you how to build your own custom build and how to test your code from anywhere in the world.\n\nWe'}
{'generated_text': 'In this course, we will teach you how to play online using JavaScript, MongoDB, and a Web API. We will be using the MongoDB'}
{'generated_text': 'In this course, we will teach you how to use your phone as a digital assistant in your everyday life. We will learn how to use your phone'}
root@hf-2:/transformers-course#
```

### fill-mask
```
root@hf-2:/transformers-course# python3 4-fill-mask.py
Some weights of the model checkpoint at distilroberta-base were not used when initializing RobertaForMaskedLM: ['roberta.pooler.dense.bias', 'roberta.pooler.dense.weight']
- This IS expected if you are initializing RobertaForMaskedLM from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing RobertaForMaskedLM from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
{'score': 0.19619670510292053, 'token': 30412, 'token_str': ' mathematical', 'sequence': 'This course will teach you all about mathematical models.'}
{'score': 0.04052688181400299, 'token': 38163, 'token_str': ' computational', 'sequence': 'This course will teach you all about computational models.'}
{'score': 0.03301766887307167, 'token': 27930, 'token_str': ' predictive', 'sequence': 'This course will teach you all about predictive models.'}
{'score': 0.03194142132997513, 'token': 745, 'token_str': ' building', 'sequence': 'This course will teach you all about building models.'}
{'score': 0.024522729218006134, 'token': 3034, 'token_str': ' computer', 'sequence': 'This course will teach you all about computer models.'}
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

### named-entity-recognition

```
root@hf-2:/transformers-course# python3 5-named-entity-recognition.py
Some weights of the model checkpoint at dbmdz/bert-large-cased-finetuned-conll03-english were not used when initializing BertForTokenClassification: ['bert.pooler.dense.bias', 'bert.pooler.dense.weight']
- This IS expected if you are initializing BertForTokenClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing BertForTokenClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
/usr/local/lib/python3.10/dist-packages/transformers/pipelines/token_classification.py:169: UserWarning: `grouped_entities` is deprecated and will be removed in version v5.0.0, defaulted to `aggregation_strategy="simple"` instead.
  warnings.warn(
{'entity_group': 'PER', 'score': 0.9941336, 'word': 'Vineeth A C', 'start': 11, 'end': 22}
{'entity_group': 'ORG', 'score': 0.99628776, 'word': 'VMware', 'start': 37, 'end': 43}
{'entity_group': 'LOC', 'score': 0.99930656, 'word': 'Bangalore', 'start': 47, 'end': 56}
{'entity_group': 'LOC', 'score': 0.99942976, 'word': 'India', 'start': 58, 'end': 63}
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

### question-answering

```
root@hf-2:/transformers-course# python3 6-question-answering.py
{'score': 0.9214025139808655, 'start': 35, 'end': 60, 'answer': 'Site Reliability Engineer'}
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

### summarization

```
root@hf-2:/transformers-course# python3 7-summarization.py
/usr/local/lib/python3.10/dist-packages/torch/_utils.py:831: UserWarning: TypedStorage is deprecated. It will be removed in the future and UntypedStorage will be the only storage class. This should only matter to you if you are using storages directly.  To access UntypedStorage directly, use tensor.untyped_storage() instead of tensor.storage()
  return self.fget.__get__(instance, owner)()
[{'summary_text': ' America has changed dramatically during recent years . The number of engineering graduates in the U.S. has declined in traditional engineering disciplines such as mechanical, civil,    electrical, chemical, and aeronautical engineering . Rapidly developing economies such as China and India continue to encourage and advance the teaching of engineering .'}]
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

### translation

```
root@hf-2:/transformers-course# python3 8-translation.py
/usr/local/lib/python3.10/dist-packages/torch/_utils.py:831: UserWarning: TypedStorage is deprecated. It will be removed in the future and UntypedStorage will be the only storage class. This should only matter to you if you are using storages directly.  To access UntypedStorage directly, use tensor.untyped_storage() instead of tensor.storage()
  return self.fget.__get__(instance, owner)()
/usr/local/lib/python3.10/dist-packages/transformers/models/marian/tokenization_marian.py:197: UserWarning: Recommended: pip install sacremoses.
  warnings.warn("Recommended: pip install sacremoses.")
[{'translation_text': 'This course is produced by Hugging Face.'}]
root@hf-2:/transformers-course#
root@hf-2:/transformers-course#
```

## References
* [Transformers and Pipeline](https://huggingface.co/learn/nlp-course/chapter1/3?fw=pt)