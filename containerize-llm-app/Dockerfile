FROM ubuntu
WORKDIR /fastapi-llm-app
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y python3
RUN apt-get install -y pip
COPY requirements.txt .
COPY model.py .
COPY main.py .
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python3 main.py