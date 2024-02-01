## Overview
In this exercise we will familiarize using the transformers-cli.

## Usage and help
* For the purpose of testing I am going to run these examples in a basic Python pod deployed on Kubernetes.
* The debug image that I am using already has Python and some other utilities pre installed.
* Instead of directly testing it on my Mac, I prefer testing them in a K8s pod!

```
root@hf-2:/# transformers-cli
usage: transformers-cli <command> [<args>]

positional arguments:
  {convert,download,env,run,serve,login,whoami,logout,repo,add-new-model,add-new-model-like,lfs-enable-largefiles,lfs-multipart-upload,pt-to-tf}
                        transformers-cli command helpers
    convert             CLI tool to run convert model from original author checkpoints to Transformers PyTorch checkpoints.
    run                 Run a pipeline through the CLI
    serve               CLI tool to run inference requests through REST and GraphQL endpoints.
    login               Log in using the same credentials as on huggingface.co
    whoami              Find out which huggingface.co account you are logged in as.
    logout              Log out
    repo                Deprecated: use `huggingface-cli` instead. Commands to interact with your huggingface.co repos.
    lfs-enable-largefiles
                        Deprecated: use `huggingface-cli` instead. Configure your repository to enable upload of files > 5GB.
    lfs-multipart-upload
                        Deprecated: use `huggingface-cli` instead. Command will get called by git-lfs, do not call it directly.
    pt-to-tf            CLI tool to run convert a transformers model from a PyTorch checkpoint to a TensorFlow checkpoint. Can also be used to validate existing weights without opening PRs, with --no-pr.

options:
  -h, --help            show this help message and exit
root@hf-2:/#
root@hf-2:/#
root@hf-2:/# transformers-cli serve --help
usage: transformers-cli <command> [<args>] serve [-h]
                                                 [--task {audio-classification,automatic-speech-recognition,conversational,depth-estimation,document-question-answering,feature-extraction,fill-mask,image-classification,image-segmentation,image-to-image,image-to-text,mask-generation,ner,object-detection,question-answering,sentiment-analysis,summarization,table-question-answering,text-classification,text-generation,text-to-audio,text-to-speech,text2text-generation,token-classification,translation,video-classification,visual-question-answering,vqa,zero-shot-audio-classification,zero-shot-classification,zero-shot-image-classification,zero-shot-object-detection}]
                                                 [--host HOST] [--port PORT] [--workers WORKERS] [--model MODEL] [--config CONFIG] [--tokenizer TOKENIZER] [--device DEVICE]

options:
  -h, --help            show this help message and exit
  --task {audio-classification,automatic-speech-recognition,conversational,depth-estimation,document-question-answering,feature-extraction,fill-mask,image-classification,image-segmentation,image-to-image,image-to-text,mask-generation,ner,object-detection,question-answering,sentiment-analysis,summarization,table-question-answering,text-classification,text-generation,text-to-audio,text-to-speech,text2text-generation,token-classification,translation,video-classification,visual-question-answering,vqa,zero-shot-audio-classification,zero-shot-classification,zero-shot-image-classification,zero-shot-object-detection}
                        The task to run the pipeline on
  --host HOST           Interface the server will listen on.
  --port PORT           Port the serving will listen to.
  --workers WORKERS     Number of http workers
  --model MODEL         Model's name or path to stored model.
  --config CONFIG       Model's config name or path to stored model.
  --tokenizer TOKENIZER
                        Tokenizer name to use.
  --device DEVICE       Indicate the device to run onto, -1 indicates CPU, >= 0 indicates GPU (default: -1)
root@hf-2:/#
```

## Run inference requests using REST endpoint
* Here we will user transformers-cli to bring up an API server that takes input, interact with the given model and returns the output.
* In the following example I am using `task=fill-mask` and `model=bert-base-uncased`.

```
root@hf-2:/# transformers-cli serve --task=fill-mask --model=bert-base-uncased
Some weights of the model checkpoint at bert-base-uncased were not used when initializing BertForMaskedLM: ['bert.pooler.dense.bias', 'bert.pooler.dense.weight', 'cls.seq_relationship.bias', 'cls.seq_relationship.weight']
- This IS expected if you are initializing BertForMaskedLM from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing BertForMaskedLM from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
INFO:     Started server process [998]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8888 (Press CTRL+C to quit)
```

* POST request to the API server from another terminal.

```
root@hf-2:/#
root@hf-2:/# curl -X POST http://localhost:8888/forward  -H "accept: application/json" -H "Content-Type: application/json" -d '{"inputs": "How [MASK] is this car?"}'
{"output":[{"score":0.5741434097290039,"token":2214,"token_str":"old","sequence":"how old is this car?"},{"score":0.19829927384853363,"token":2502,"token_str":"big","sequence":"how big is this car?"},{"score":0.02225376106798649,"token":6450,"token_str":"expensive","sequence":"how expensive is this car?"},{"score":0.017738202586770058,"token":2919,"token_str":"bad","sequence":"how bad is this car?"},{"score":0.015539600513875484,"token":2146,"token_str":"long","sequence":"how long is this car?"}]}root@hf-2:/#
root@hf-2:/#
root@hf-2:/#
```

* Using jq for pretty print.

```
root@hf-2:/# apt-get install -y jq
root@hf-2:/#
root@hf-2:/# curl -X POST http://localhost:8888/forward  -H "accept: application/json" -H "Content-Type: application/json" -d '{"inputs": "How [MASK] is this car?"}' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   539  100   502  100    37   8401    619 --:--:-- --:--:-- --:--:--  9135
{
  "output": [
    {
      "score": 0.5741434097290039,
      "token": 2214,
      "token_str": "old",
      "sequence": "how old is this car?"
    },
    {
      "score": 0.19829927384853363,
      "token": 2502,
      "token_str": "big",
      "sequence": "how big is this car?"
    },
    {
      "score": 0.02225376106798649,
      "token": 6450,
      "token_str": "expensive",
      "sequence": "how expensive is this car?"
    },
    {
      "score": 0.017738202586770058,
      "token": 2919,
      "token_str": "bad",
      "sequence": "how bad is this car?"
    },
    {
      "score": 0.015539600513875484,
      "token": 2146,
      "token_str": "long",
      "sequence": "how long is this car?"
    }
  ]
}
root@hf-2:/#
root@hf-2:/#
```

## Next steps
* We will containerize this model and run it on a Kubernetes cluster.