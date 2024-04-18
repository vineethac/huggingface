## Overview
* In this section we will take a look at deploying the containerized llm app to a Kubernetes cluster.
* We will see the storage disk space requirements on the worker nodes.
* And, we will also add readiness and liveness probes to the deployment resource.

## Access to a Kubernetes cluster
* I am using a Tanzu Kubernetes Cluster (TKC) for this exercise.
* Following is my TKC spec:

```
❯ kgtkca | grep vineetha-poc
vineetha-poc                                 tkc01                             2023-11-29T12:59:59Z   v1.23.8+vmware.3-tkg.1             3     3        True    running
❯
❯ k get tkc tkc01 -n vineetha-poc -oyaml | k neat
apiVersion: run.tanzu.vmware.com/v1alpha2
kind: TanzuKubernetesCluster
metadata:
  labels:
    run.tanzu.vmware.com/tkr: v1.23.8---vmware.3-tkg.1
  name: tkc01
  namespace: vineetha-poc
spec:
  distribution:
    fullVersion: v1.23.8+vmware.3-tkg.1
    version: ""
  settings:
    network:
      cni:
        name: antrea
      pods:
        cidrBlocks:
        - 192.168.0.0/16
      serviceDomain: cluster.local
      services:
        cidrBlocks:
        - 10.96.0.0/12
  topology:
    controlPlane:
      replicas: 3
      storageClass: wcp-ccs-default
      tkr:
        reference:
          name: v1.23.8---vmware.3-tkg.1
      vmClass: best-effort-2xlarge
    nodePools:
    - name: worker-nodepool-a1
      replicas: 3
      storageClass: wcp-ccs-default
      tkr:
        reference:
          name: v1.23.8---vmware.3-tkg.1
      vmClass: best-effort-2xlarge
      volumes:
      - capacity:
          storage: 256Gi
        mountPath: /var/lib/containerd
        name: containerd
❯
❯ k get vm -n vineetha-poc -o wide
NAME                                             POWERSTATE   CLASS                 IMAGE                                                    PRIMARY-IP      AGE
tkc01-control-plane-49jx4                        poweredOn    best-effort-2xlarge   ob-20953521-tkgs-ova-photon-3-v1.23.8---vmware.3-tkg.1   172.29.13.99    97d
tkc01-control-plane-m8wmt                        poweredOn    best-effort-2xlarge   ob-20953521-tkgs-ova-photon-3-v1.23.8---vmware.3-tkg.1   172.29.13.102   105d
tkc01-control-plane-z6gxx                        poweredOn    best-effort-2xlarge   ob-20953521-tkgs-ova-photon-3-v1.23.8---vmware.3-tkg.1   172.29.13.101   97d
tkc01-worker-nodepool-a1-pqq7j-dc6957d97-8gjn8   poweredOn    best-effort-2xlarge   ob-20953521-tkgs-ova-photon-3-v1.23.8---vmware.3-tkg.1   172.29.13.103   21d
tkc01-worker-nodepool-a1-pqq7j-dc6957d97-c9nfq   poweredOn    best-effort-2xlarge   ob-20953521-tkgs-ova-photon-3-v1.23.8---vmware.3-tkg.1   172.29.13.104   21d
tkc01-worker-nodepool-a1-pqq7j-dc6957d97-cngff   poweredOn    best-effort-2xlarge   ob-20953521-tkgs-ova-photon-3-v1.23.8---vmware.3-tkg.1   172.29.13.100   21d
❯
❯ kg vmclass best-effort-2xlarge
NAME                  CPU   MEMORY   AGE
best-effort-2xlarge   8     64Gi     3y66d
❯
❯ KUBECONFIG=gckubeconfig k get node
NAME                                             STATUS   ROLES                  AGE    VERSION
tkc01-control-plane-49jx4                        Ready    control-plane,master   97d    v1.23.8+vmware.3
tkc01-control-plane-m8wmt                        Ready    control-plane,master   105d   v1.23.8+vmware.3
tkc01-control-plane-z6gxx                        Ready    control-plane,master   97d    v1.23.8+vmware.3
tkc01-worker-nodepool-a1-pqq7j-dc6957d97-8gjn8   Ready    <none>                 21d    v1.23.8+vmware.3
tkc01-worker-nodepool-a1-pqq7j-dc6957d97-c9nfq   Ready    <none>                 21d    v1.23.8+vmware.3
tkc01-worker-nodepool-a1-pqq7j-dc6957d97-cngff   Ready    <none>                 21d    v1.23.8+vmware.3
❯
```

* As you can see, I have 3 control plane nodes, and 3 worker nodes.
* Each node is of size `best-effort-2xlarge` which has 8 vCPU and 64Gi of memory.
* In the TKC spec you can see that I've attached 256Gi storage volumes to the worker nodes that is mounted at `/var/lib/containerd`. The worker nodes on which these llm pods are running should have enough storage space. Otherwise you may notice these pods getting stuck/ restarting/ unknownstatus. If the worker nodes run out of the storage disk space, you will see pods getting evicted with warnings `The node was low on resource: ephemeral-storage`.


## Deploy the LLM app 
* The deployment and service yaml spec are given in `fastapi-llm-app-deploy-cpu.yaml`.
* This works on a CPU powered Kubernetes cluster. Additional configurations might be required if you want to run this on a GPU powered cluster.

```
❯ KUBECONFIG=gckubeconfig k apply -f fastapi-llm-app-deploy-cpu.yaml
```

* Once the above yaml spec is applied, you will see the following resources.

```
❯ KUBECONFIG=gckubeconfig k get deploy fastapi-llm-app
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
fastapi-llm-app   2/2     2            2           21d
❯
❯ KUBECONFIG=gckubeconfig k get pods | grep fastapi-llm-app
fastapi-llm-app-758c7c58f7-79gmq                               1/1     Running   1 (71m ago)    13d
fastapi-llm-app-758c7c58f7-gqdc6                               1/1     Running   1 (99m ago)    13d
❯
❯ KUBECONFIG=gckubeconfig k get svc fastapi-llm-app
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
fastapi-llm-app   LoadBalancer   10.110.228.33   10.216.24.104   5000:30590/TCP   5h24m
❯
```

* Here we've exposed the llm app using a service of type `LoadBalancer`. 
* You can consider creating an ingress resource to expose this service with an FQDN.

## Validation
* I am just doing a curl against the `EXTERNAL-IP` of the above mentioned `fastapi-llm-app` service.

```
❯ curl http://10.216.24.104:5000/ask -X POST -H "Content-Type: application/json" -d '{"text":"list comprehension examples in python"}'

{"response":" List comprehensions are a concise way to create lists in Python. Here are some common examples:\n\n1. Creating a list of squares:\n\n```python\nnumbers = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in numbers]\nprint(squares)  # Output: [1, 4, 9, 16, 25]\n```\n\n2. Creating a list of even numbers:\n\n```python\nnumbers = [1, 2, 3, 4, 5]\nevens = [x for x in numbers if x % 2 == 0]\nprint(evens)  # Output: [2, 4]\n```\n\n3. Creating a list of tuples:\n\n```python\nnumbers = [1, 2, 3, 4, 5]\ntuples = [(x, x**2) for x in numbers]\nprint(tuples)  # Output: [(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]\n```\n\n4. Creating an empty list and filling it with elements:\n\n```python\nempty_list = []\nfilled_list = [i for i in range(10)]\nprint(filled_list)  # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\n```\n\n5. Flattening a list of lists:\n\n```python\nnested_list = [[1, 2], [3, 4], [5, 6]]\nflat_list = [element for sublist in nested_list for element in sublist]\nprint(flat_list)  # Output: [1, 2, 3, 4, 5, 6]\n```\n\n6. Filtering and mapping at the same time:\n\n```python\nnumbers = [1, 2, 3, 4, 5]\nfiltered_and_mapped = [x**2 if x > 2 else x for x in numbers]\nprint(filtered_and_mapped)  # Output: [4, 9, 9, 16, 5]\n```"}
```

* Once you print it, it will look like this!

```
List comprehensions are a concise way to create lists in Python. Here are some common examples:
```
1. Creating a list of squares:

```python
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares)  # Output: [1, 4, 9, 16, 25]
```

2. Creating a list of even numbers:

```python
numbers = [1, 2, 3, 4, 5]
evens = [x for x in numbers if x % 2 == 0]
print(evens)  # Output: [2, 4]
```

3. Creating a list of tuples:

```python
numbers = [1, 2, 3, 4, 5]
tuples = [(x, x**2) for x in numbers]
print(tuples)  # Output: [(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]
```

4. Creating an empty list and filling it with elements:

```python
empty_list = []
filled_list = [i for i in range(10)]
print(filled_list)  # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

5. Flattening a list of lists:

```python
nested_list = [[1, 2], [3, 4], [5, 6]]
flat_list = [element for sublist in nested_list for element in sublist]
print(flat_list)  # Output: [1, 2, 3, 4, 5, 6]
```

6. Filtering and mapping at the same time:

```python
numbers = [1, 2, 3, 4, 5]
filtered_and_mapped = [x**2 if x > 2 else x for x in numbers]
print(filtered_and_mapped)  # Output: [4, 9, 9, 16, 5]
``` 

* Note that the API is not returning streaming response. It waits for few seconds/ minutes based on the user prompt, and then returns the complete response provided by the llm.

## Observations
* Here we will take a look at the readiness and liveness probes.
* In the deployment yaml spec we have already added both the probes.

```
        readinessProbe:
          failureThreshold: 5
          httpGet:
            path: /healthz
            port: 5000
            scheme: HTTP
          initialDelaySeconds: 600
          periodSeconds: 120
          successThreshold: 1
          timeoutSeconds: 60

        livenessProbe:
          exec:
            command:
            - python3
            - liveness.py
          failureThreshold: 3
          initialDelaySeconds: 600
          periodSeconds: 180
          successThreshold: 1
          timeoutSeconds: 300          
```

* The readiness probe basically invokes the `/healthz` endpoint exposed by the FastAPI app. This will make sure the FastAPI itself is healthy/ responding to the API calls.
* The liveness probe invokes `liveness.py` script within the app. The script invokes the `/ask` endpoint which interacts with the LLM and returns the response. This will make sure the LLM is responding to the user queries. For some reason if the llm is not responding/ hangs, the liveness probe will fail and eventually it will restart the container. 
* If you look at the llm app pod logs, you can see the probes getting invoked.

```
INFO:     192.168.4.1:55476 - "GET /healthz HTTP/1.1" 200 OK
2024-04-18 13:29:19 fastapi-llm-app-758c7c58f7-gqdc6 root[25] INFO User prompt: select head or tail randomly. strictly respond only in one word.         no explanations needed.
2024-04-18 13:29:19 fastapi-llm-app-758c7c58f7-gqdc6 root[25] INFO Model: mistralai/Mistral-7B-Instruct-v0.2
Setting `pad_token_id` to `eos_token_id`:2 for open-end generation.
2024-04-18 13:29:23 fastapi-llm-app-758c7c58f7-gqdc6 root[25] INFO LLM response:  Head.
2024-04-18 13:29:23 fastapi-llm-app-758c7c58f7-gqdc6 root[25] INFO FastAPI response:  Head.
INFO:     127.0.0.1:34694 - "POST /ask HTTP/1.1" 200 OK
```

* Following is a sample pod events when the liveness and readiness probe failed.

```
Events:
  Type     Reason     Age   From     Message
  ----     ------     ----  ----     -------
  Warning  Unhealthy  14m   kubelet  Liveness probe failed: Traceback (most recent call last):
  Normal   Killing    2m31s                  kubelet  Container fastapi-llm-app failed liveness probe, will be restarted
  Warning  Unhealthy  2m31s (x8 over 24m)    kubelet  Readiness probe failed: Get "http://192.168.4.15:5000/healthz": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
  Warning  Unhealthy  2m31s (x2 over 7m31s)  kubelet  Liveness probe failed: command "python3 liveness.py" timed out
  Warning  Unhealthy  2m                     kubelet  Readiness probe failed: Get "http://192.168.4.15:5000/healthz": read tcp 192.168.4.1:48336->192.168.4.15:5000: read: connection reset by peer
  Warning  Unhealthy  2m                     kubelet  Readiness probe failed: Get "http://192.168.4.15:5000/healthz": dial tcp 192.168.4.15:5000: connect: connection refused
  Normal   Pulling    2m (x2 over 13d)       kubelet  Pulling image "vineethac/fastapi-llm-app:latest"
  Normal   Created    119s (x2 over 13d)     kubelet  Created container fastapi-llm-app
  Normal   Started    119s (x2 over 13d)     kubelet  Started container fastapi-llm-app
  Normal   Pulled     119s                   kubelet  Successfully pulled image "vineethac/fastapi-llm-app:latest" in 1.014871187s
```

## References



## To-Do
* Add a metrics end point to the llm app to get visibility to the FastAPI operations.