FROM python:3.9

RUN pwd
RUN ls -la

WORKDIR /usr/src/app
COPY . .

RUN pwd
RUN ls -la

RUN pip install requests

ENTRYPOINT ["python", "/usr/src/app/script.py"]