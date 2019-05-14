FROM ubuntu:latest

RUN apt-get update && \
	apt-get install python3 -y && \
	apt-get install python3-pip -y

COPY . /home/

WORKDIR /home/

RUN pip3 install -r requirements.txt

EXPOSE 5000

# ENTRYPOINT gunicorn --chdir app main:app --bind localhost:5000
CMD python3 app/main.py
