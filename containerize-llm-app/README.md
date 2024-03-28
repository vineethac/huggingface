## Overview
* In this exercise we will add an API endpoint for the LLM from Hugging Face using FastAPI.
* We will also containerize this LLM app using Docker.

## How it works
* Here we have `model.py` which serves the `model_pipeline` function. 
* In this case we are using the Mistral Instruct model from Hugging Face.
* The `main.py` implements the FastAPI, and `/ask` will invoke the `model_pipeline` function which interacts with the `Mistral Instruct` model and returns response.
* And, we have containerized this FastAPI LLM app using the Dockerfile.
* You can pull the image by: `docker pull vineethac/fastapi-llm-app`

## Deploy on Kubernetes
* Deploy as a pod. This is just for quick testing purpose!

```
❯ KUBECONFIG=gckubeconfig k run hf-11 --image=vineethac/fastapi-llm-app:latest --image-pull-policy=Always
pod/hf-11 created
❯ KUBECONFIG=gckubeconfig kg po hf-11
NAME    READY   STATUS              RESTARTS   AGE
hf-11   0/1     ContainerCreating   0          2m23s
❯
❯ KUBECONFIG=gckubeconfig kg po hf-11
NAME    READY   STATUS    RESTARTS   AGE
hf-11   1/1     Running   0          26m
❯
❯ KUBECONFIG=gckubeconfig k logs hf-11 -f
Downloading shards: 100%|██████████| 3/3 [02:29<00:00, 49.67s/it]
Loading checkpoint shards: 100%|██████████| 3/3 [00:03<00:00,  1.05s/it]
INFO:     Will watch for changes in these directories: ['/fastapi-llm-app']
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [7] using WatchFiles
Loading checkpoint shards: 100%|██████████| 3/3 [00:11<00:00,  3.88s/it]
INFO:     Started server process [25]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
2024-03-28 08:19:12 hf-11 watchfiles.main[7] INFO 3 changes detected
2024-03-28 08:19:48 hf-11 root[25] INFO User prompt: select head or tail randomly. strictly respond only in one word. no explanations needed.
2024-03-28 08:19:48 hf-11 root[25] INFO Model: mistralai/Mistral-7B-Instruct-v0.2
Setting `pad_token_id` to `eos_token_id`:2 for open-end generation.
2024-03-28 08:19:54 hf-11 root[25] INFO LLM response:  Head.
2024-03-28 08:19:54 hf-11 root[25] INFO FastAPI response:  Head.
INFO:     127.0.0.1:53904 - "POST /ask HTTP/1.1" 200 OK
INFO:     127.0.0.1:55264 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:43342 - "GET /healthz HTTP/1.1" 200 OK
```

## Sample test
* For testing, I just deployed it as a pod on my Kubernetes cluster, did exec into it, and curl against the exposed APIs.

```
❯ KUBECONFIG=gckubeconfig k exec -it hf-11 -- bash
root@hf-11:/fastapi-llm-app#
root@hf-11:/fastapi-llm-app# curl -d '{"text":"select head or tail randomly. strictly respond only in one word. no explanations needed."}' -H "Content-Type: application/json" -X POST http://localhost:5000/ask
{"response":" Head."}root@hf-11:/fastapi-llm-app#
root@hf-11:/fastapi-llm-app# curl localhost:5000
"Welcome to FastAPI for your local LLM!"root@hf-11:/fastapi-llm-app#
root@hf-11:/fastapi-llm-app#
root@hf-11:/fastapi-llm-app# curl localhost:5000/healthz
{"Status":"OK"}root@hf-11:/fastapi-llm-app#
root@hf-11:/fastapi-llm-app#
```

## References

