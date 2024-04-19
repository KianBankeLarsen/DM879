FROM python:3.10.14

WORKDIR /poker

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY Poker.py .
COPY lib .

ENTRYPOINT ["python3", "Poker.py"]