FROM python:3.9

WORKDIR /usr/src/app
COPY . .

RUN pip install requests

ENTRYPOINT ["python", "/usr/src/app/script.py"]