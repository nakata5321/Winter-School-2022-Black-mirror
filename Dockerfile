FROM python:3.9-buster
RUN apt-get update
RUN mkdir qr_script
WORKDIR qr_script
COPY . .
RUN pip3 install -r requirements.txt

CMD ["python", "main.py" ]