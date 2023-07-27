FROM python:3.10.9

COPY . /usr/src

RUN pip install -r "/usr/src/requirements.txt"

WORKDIR /usr/src

CMD ["python", "main.py"]