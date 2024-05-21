FROM python:3.10.14

WORKDIR /poker

RUN mkdir pickle

COPY . .

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]