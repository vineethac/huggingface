## Overview
* In this exercise we will add an API endpoint for the LLM from Hugging Face using FastAPI.
* We will also containerize this LLM app using Docker.

## Example

```
root@hf-7:/fastapi# curl http://localhost:5000
"Welcome to FastAPI for your local LLM!"
root@hf-7:/fastapi#
root@hf-7:/fastapi#
root@hf-7:/fastapi# curl http://localhost:5000/healthz
{"Status":"OK"}
root@hf-7:/fastapi#
root@hf-7:/fastapi#
root@hf-7:/fastapi# curl -d '{"text":"select head or tail randomly. strictly respond only in one word. no explanations needed."}' -H "Content-Type: application/json" -X POST http://localhost:5000/ask -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1:5000...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /ask HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.81.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 99
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< date: Wed, 27 Mar 2024 12:59:03 GMT
< server: uvicorn
< content-length: 21
< content-type: application/json
<
* Connection #0 to host localhost left intact
{"response":" Head."}
root@hf-7:/fastapi#
root@hf-7:/fastapi#
```

## References

