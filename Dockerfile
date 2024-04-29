FROM python:3.10.14

WORKDIR /poker

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY python_skeleton python_skeleton

ENTRYPOINT ["python3", "python_skeleton/engine.py"]